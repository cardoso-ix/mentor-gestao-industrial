"""
Módulo RAG — ingestão e consulta de documentos PDF na base de conhecimento.

Usa ChromaDB para armazenar embeddings e sentence-transformers para gerar
vetores localmente (sem custo de API).
"""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any

import chromadb
from chromadb.config import Settings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from pypdf import PdfReader

import config

# Modelo de embeddings carregado sob demanda (evita carregar no import)
_modelo_embeddings = None


def _obter_modelo_embeddings():
    """Carrega o modelo de embeddings apenas uma vez (singleton)."""
    global _modelo_embeddings
    if _modelo_embeddings is None:
        from sentence_transformers import SentenceTransformer

        _modelo_embeddings = SentenceTransformer(config.EMBEDDING_MODEL)
    return _modelo_embeddings


def _calcular_hash_arquivo(caminho: Path) -> str:
    """Calcula hash MD5 do arquivo para detectar alterações."""
    hasher = hashlib.md5()
    with open(caminho, "rb") as arquivo:
        for bloco in iter(lambda: arquivo.read(8192), b""):
            hasher.update(bloco)
    return hasher.hexdigest()


def _carregar_manifesto() -> dict[str, str]:
    """Lê o manifesto de PDFs já indexados (nome -> hash)."""
    if not config.INDEX_MANIFEST_PATH.exists():
        return {}
    try:
        return json.loads(config.INDEX_MANIFEST_PATH.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError):
        return {}


def _salvar_manifesto(manifesto: dict[str, str]) -> None:
    """Salva o manifesto de indexação no disco."""
    config.INDEX_MANIFEST_PATH.parent.mkdir(parents=True, exist_ok=True)
    config.INDEX_MANIFEST_PATH.write_text(
        json.dumps(manifesto, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )


def _obter_cliente_chroma() -> chromadb.ClientAPI:
    """Cria ou retorna o cliente ChromaDB com persistência em disco."""
    config.CHROMA_PERSIST_DIR.mkdir(parents=True, exist_ok=True)
    return chromadb.PersistentClient(
        path=str(config.CHROMA_PERSIST_DIR),
        settings=Settings(anonymized_telemetry=False),
    )


def _obter_colecao():
    """Retorna a coleção do ChromaDB usada para os PDFs."""
    cliente = _obter_cliente_chroma()
    return cliente.get_or_create_collection(
        name=config.CHROMA_COLLECTION_NAME,
        metadata={"hnsw:space": "cosine"},
    )


def _extrair_texto_pdf(caminho: Path) -> str:
    """Extrai todo o texto de um arquivo PDF."""
    leitor = PdfReader(str(caminho))
    paginas = []
    for pagina in leitor.pages:
        texto = pagina.extract_text()
        if texto:
            paginas.append(texto)
    return "\n\n".join(paginas)


def _dividir_texto(texto: str, nome_arquivo: str, categoria: str = "geral") -> list[dict[str, Any]]:
    """Divide o texto em pedaços menores (chunks) para indexação."""
    divisor = RecursiveCharacterTextSplitter(
        chunk_size=config.CHUNK_SIZE,
        chunk_overlap=config.CHUNK_OVERLAP,
        separators=["\n\n", "\n", ". ", " ", ""],
    )
    pedacos = divisor.split_text(texto)
    documentos = []
    for indice, pedaco in enumerate(pedacos):
        if pedaco.strip():
            documentos.append(
                {
                    "id": f"{nome_arquivo}__chunk_{indice}",
                    "texto": pedaco,
                    "metadados": {
                        "fonte": nome_arquivo,
                        "categoria": categoria,
                        "chunk_index": indice,
                    },
                }
            )
    return documentos


def _remover_documentos_fonte(colecao, nome_arquivo: str) -> None:
    """Remove todos os chunks de um PDF específico da coleção."""
    try:
        resultado = colecao.get(where={"fonte": nome_arquivo})
        if resultado and resultado.get("ids"):
            colecao.delete(ids=resultado["ids"])
    except Exception:
        # Se a coleção estiver vazia ou o filtro falhar, ignoramos
        pass


def _nome_relativo_pdf(caminho: Path) -> str:
    return str(caminho.relative_to(config.KNOWLEDGE_BASE_DIR)).replace("\\", "/")


def _precisa_indexacao(pdfs: list[Path], manifesto: dict[str, str], forcar: bool) -> bool:
    """Verifica se há PDFs novos/alterados ou removidos sem carregar embeddings."""
    if forcar and pdfs:
        return True
    nomes_atuais = {_nome_relativo_pdf(p) for p in pdfs}
    if any(nome not in nomes_atuais for nome in manifesto):
        return True
    for caminho_pdf in pdfs:
        nome = _nome_relativo_pdf(caminho_pdf)
        hash_atual = _calcular_hash_arquivo(caminho_pdf)
        if manifesto.get(nome) != hash_atual:
            return True
    return False


def garantir_base_indexada(forcar: bool = False) -> dict[str, Any]:
    """Garante que a base RAG está atualizada (só na análise, não na abertura)."""
    return indexar_pdfs(forcar=forcar)


def indexar_pdfs(forcar: bool = False) -> dict[str, Any]:
    """
    Indexa os PDFs da pasta knowledge_base no ChromaDB.

    Args:
        forcar: Se True, reindexa todos os PDFs mesmo sem alteração.

    Returns:
        Dicionário com estatísticas da indexação.
    """
    config.KNOWLEDGE_BASE_DIR.mkdir(parents=True, exist_ok=True)
    config.CHROMA_PERSIST_DIR.mkdir(parents=True, exist_ok=True)

    pdfs = sorted(config.KNOWLEDGE_BASE_DIR.rglob("*.pdf"))
    manifesto = _carregar_manifesto()

    if not _precisa_indexacao(pdfs, manifesto, forcar):
        try:
            chunks = _obter_colecao().count()
        except Exception:
            chunks = 0
        return {
            "total_pdfs": len(pdfs),
            "indexados": 0,
            "ignorados": len(pdfs),
            "erros": [],
            "chunks_total": chunks,
        }

    colecao = _obter_colecao()
    modelo = None

    indexados = 0
    ignorados = 0
    erros: list[str] = []

    for caminho_pdf in pdfs:
        rel = caminho_pdf.relative_to(config.KNOWLEDGE_BASE_DIR)
        nome = str(rel).replace("\\", "/")
        categoria = rel.parts[0] if len(rel.parts) > 1 else "geral"
        hash_atual = _calcular_hash_arquivo(caminho_pdf)

        # Pula PDFs que não mudaram (a menos que force reindexação)
        if not forcar and manifesto.get(nome) == hash_atual:
            ignorados += 1
            continue

        try:
            texto = _extrair_texto_pdf(caminho_pdf)
            if not texto.strip():
                erros.append(f"{nome}: PDF sem texto extraível")
                continue

            documentos = _dividir_texto(texto, nome, categoria)
            if not documentos:
                erros.append(f"{nome}: nenhum chunk gerado")
                continue

            # Remove versão antiga antes de inserir a nova
            _remover_documentos_fonte(colecao, nome)

            if modelo is None:
                modelo = _obter_modelo_embeddings()

            textos = [doc["texto"] for doc in documentos]
            ids = [doc["id"] for doc in documentos]
            metadados = [doc["metadados"] for doc in documentos]
            embeddings = modelo.encode(textos, show_progress_bar=False).tolist()

            colecao.add(
                ids=ids,
                documents=textos,
                embeddings=embeddings,
                metadatas=metadados,
            )

            manifesto[nome] = hash_atual
            indexados += 1

        except Exception as exc:
            erros.append(f"{nome}: {exc}")

    # Remove do manifesto PDFs que foram deletados da pasta
    nomes_atuais = {str(p.relative_to(config.KNOWLEDGE_BASE_DIR)).replace("\\", "/") for p in pdfs}
    for nome_removido in list(manifesto.keys()):
        if nome_removido not in nomes_atuais:
            _remover_documentos_fonte(colecao, nome_removido)
            del manifesto[nome_removido]

    _salvar_manifesto(manifesto)

    return {
        "total_pdfs": len(pdfs),
        "indexados": indexados,
        "ignorados": ignorados,
        "erros": erros,
        "chunks_total": colecao.count(),
    }


def consultar_base(
    query: str,
    top_k: int | None = None,
    categoria: str | None = None,
) -> str:
    """
    Busca os trechos mais relevantes na base de conhecimento.

    Args:
        query: Texto da pergunta ou situação do usuário.
        top_k: Quantidade de trechos a retornar (padrão: config.RAG_TOP_K).
        categoria: Filtrar por pasta (normas, gestao, processos). Se vazio, busca em tudo.

    Returns:
        Texto formatado com os trechos encontrados, ou string vazia se não houver.
    """
    if not query.strip():
        return ""

    colecao = _obter_colecao()
    if colecao.count() == 0:
        return ""

    k = top_k or config.RAG_TOP_K
    modelo = _obter_modelo_embeddings()
    embedding_query = modelo.encode([query], show_progress_bar=False).tolist()

    filtro = {"categoria": categoria} if categoria else None
    n_results = min(k, colecao.count())

    if filtro:
        try:
            count_cat = colecao.count(where=filtro)
            if count_cat > 0:
                n_results = min(k, count_cat)
                resultados = colecao.query(
                    query_embeddings=embedding_query,
                    n_results=n_results,
                    where=filtro,
                )
            else:
                resultados = colecao.query(
                    query_embeddings=embedding_query,
                    n_results=n_results,
                )
        except Exception:
            resultados = colecao.query(
                query_embeddings=embedding_query,
                n_results=n_results,
            )
    else:
        resultados = colecao.query(
            query_embeddings=embedding_query,
            n_results=n_results,
        )

    documentos = resultados.get("documents", [[]])[0]
    metadados = resultados.get("metadatas", [[]])[0]

    if not documentos:
        return ""

    trechos = []
    for indice, doc in enumerate(documentos):
        meta = metadados[indice] if metadados else {}
        fonte = meta.get("fonte", "desconhecido")
        cat = meta.get("categoria", "")
        prefixo = f"[{cat}] " if cat else ""
        trechos.append(f"[Fonte: {prefixo}{fonte}]\n{doc}")

    return "\n\n---\n\n".join(trechos)


def obter_status_base() -> dict[str, Any]:
    """Retorna informações sobre o estado atual da base de conhecimento."""
    config.KNOWLEDGE_BASE_DIR.mkdir(parents=True, exist_ok=True)
    pdfs = list(config.KNOWLEDGE_BASE_DIR.rglob("*.pdf"))
    manifesto = _carregar_manifesto()

    try:
        colecao = _obter_colecao()
        chunks = colecao.count()
    except Exception:
        chunks = 0

    categorias: dict[str, int] = {}
    for p in pdfs:
        rel = p.relative_to(config.KNOWLEDGE_BASE_DIR)
        cat = rel.parts[0] if len(rel.parts) > 1 else "geral"
        categorias[cat] = categorias.get(cat, 0) + 1

    return {
        "total_pdfs": len(pdfs),
        "pdfs_indexados": len(manifesto),
        "nomes_pdfs": [str(p.relative_to(config.KNOWLEDGE_BASE_DIR)).replace("\\", "/") for p in pdfs],
        "chunks_total": chunks,
        "categorias": categorias,
    }
