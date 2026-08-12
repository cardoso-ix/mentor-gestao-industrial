"""Limpeza e formatação de texto para exibição profissional na interface."""

from __future__ import annotations

import html
import re

_PADROES_ERRO = (
    r"litellm\.?",
    r"RateLimitError",
    r"GroqException",
    r"OpenRouterException",
    r"rate_limit",
    r"síntese automática indisponível",
    r"Relatório simplificado",
    r"organization\s+:",
    r"tokens per day",
    r"console\.groq\.com",
    r"openrouter\.ai",
)

_MAPA_TIPO = {
    "lideranca": "liderança",
    "comunicacao": "comunicação",
    "conflito": "conflito interpessoal",
    "desempenho": "desempenho",
    "processo": "processo",
    "seguranca": "segurança do trabalho",
}


def limpar_markdown(texto: str) -> str:
    """Remove formatação markdown e artefatos comuns dos agentes."""
    if not texto:
        return ""
    t = str(texto)
    t = re.sub(r"```[\s\S]*?```", "", t)
    t = re.sub(r"`([^`]+)`", r"\1", t)
    t = re.sub(r"\*\*([^*]+)\*\*", r"\1", t)
    t = re.sub(r"\*([^*]+)\*", r"\1", t)
    t = re.sub(r"\*\*", "", t)
    t = re.sub(r"#{1,6}\s*\d*\.?\s*", "", t)
    t = re.sub(r"^\s*[-•]\s*#+\s*", "- ", t, flags=re.M)
    t = re.sub(r"^\s*[-•]\s+", "- ", t, flags=re.M)
    t = re.sub(r"[ \t]+\n", "\n", t)
    t = re.sub(r"\n{3,}", "\n\n", t)
    return t.strip()


def contem_erro_tecnico(texto: str) -> bool:
    if not texto:
        return False
    for padrao in _PADROES_ERRO:
        if re.search(padrao, texto, re.I):
            return True
    if ")." in texto and len(texto) < 80:
        return True
    return False


def sanitizar_para_exibicao(texto: str) -> str:
    if not texto:
        return ""
    linhas = []
    for linha in limpar_markdown(texto).split("\n"):
        linha = linha.strip()
        if not linha or contem_erro_tecnico(linha):
            continue
        linhas.append(linha)
    return "\n\n".join(linhas).strip()


def _titulo_secao(linha: str) -> str | None:
    """Detecta se a linha é um título de seção."""
    linha = linha.strip()
    if not linha or len(linha) > 120:
        return None
    if linha.endswith(":") and not linha.startswith("-"):
        titulo = linha[:-1].strip()
        if titulo and len(titulo.split()) <= 12:
            return titulo
    if re.match(r"^(passo\s+\d+|plano de a[cç][aã]o)\b", linha, re.I):
        return None
    if re.match(r"^\d+[\.\)]\s+\S", linha):
        return re.sub(r"^\d+[\.\)]\s+", "", linha).strip()
    if re.match(r"^[A-ZÁÉÍÓÚÂÊÔÃÕÇ][\w\s\-]{4,}$", linha) and len(linha.split()) <= 10:
        if linha.endswith(":"):
            return linha[:-1].strip()
        if not linha.endswith("."):
            return linha
    return None


def formatar_em_blocos(texto: str) -> list[dict[str, str]]:
    """
    Converte saída dos agentes em blocos para renderização (título, parágrafo, item).
    """
    texto = sanitizar_para_exibicao(texto)
    if not texto:
        return []

    blocos: list[dict[str, str]] = []
    buffer: list[str] = []

    def flush_paragrafo():
        if buffer:
            par = "\n".join(buffer).strip()
            if par and not contem_erro_tecnico(par):
                blocos.append({"tipo": "paragrafo", "texto": par})
            buffer.clear()

    for linha in texto.split("\n"):
        linha = linha.strip()
        if not linha:
            flush_paragrafo()
            continue

        if linha.startswith("- "):
            flush_paragrafo()
            item = linha[2:].strip()
            if item:
                blocos.append({"tipo": "item", "texto": item})
            continue

        if re.match(r"^passo\s+\d+", linha, re.I) or re.match(r"^\d+[\.\)]\s+", linha):
            flush_paragrafo()
            blocos.append({"tipo": "item", "texto": re.sub(r"^\d+[\.\)]\s+", "", linha).strip()})
            continue

        titulo = _titulo_secao(linha)
        if titulo and len(titulo) < 80:
            flush_paragrafo()
            blocos.append({"tipo": "titulo", "texto": titulo})
            continue

        buffer.append(linha)

    flush_paragrafo()
    return blocos


def truncar_em_frase(texto: str, limite: int) -> str:
    """Corta texto no limite sem partir palavra nem frase no meio."""
    texto = (texto or "").strip()
    if not texto or len(texto) <= limite:
        return texto

    janela = texto[:limite]
    melhor = -1
    for sep in (". ", "! ", "? ", ".\n", "!\n", "?\n"):
        idx = janela.rfind(sep)
        if idx > melhor and idx >= 60:
            melhor = idx
    if melhor >= 0:
        return janela[: melhor + 1].strip()

    corte = janela.rsplit(" ", 1)[0].rstrip(".,;:")
    return (corte or janela.rstrip()) + "..."


def _primeiro_paragrafo_util(texto: str) -> str:
    """Pega o primeiro parágrafo substantivo (pula títulos curtos)."""
    for linha in limpar_markdown(texto or "").split("\n"):
        linha = linha.strip()
        if not linha or linha.endswith(":"):
            continue
        if len(linha) <= 40:
            continue
        if linha.startswith("- ") and len(linha) < 60:
            continue
        return linha
    return limpar_markdown(texto or "").strip()


def _formatar_prioridade(passo: str) -> str:
    """Normaliza o 1º passo do plano para a síntese executiva."""
    acao = limpar_markdown(passo or "")
    if not acao:
        return ""
    acao = re.sub(r"\s*—\s*-\s*O que fazer:\s*", ": ", acao, flags=re.I)
    acao = re.sub(r"\s*-\s*O que fazer:\s*", ": ", acao, flags=re.I)
    acao = re.sub(r"\s{2,}", " ", acao).strip()
    return truncar_em_frase(acao, 420)


def montar_visao_geral_profissional(
    analise: dict,
    plano_acao: str = "",
    estrategia: str = "",
) -> str:
    """
    Síntese executiva formal — não repete conteúdo das abas.
    """
    from ui.export_utils import extrair_passos_plano

    partes: list[str] = []

    resumo = limpar_markdown((analise or {}).get("resumo", ""))
    if resumo:
        partes.append(resumo)

    tipo = _MAPA_TIPO.get((analise or {}).get("tipo_problema", "").lower(), "gestão")
    comp = (analise or {}).get("complexidade", "média")
    partes.append(f"Classificação: {tipo} — complexidade {comp}.")

    trecho = _primeiro_paragrafo_util(estrategia or "")
    if trecho:
        partes.append(truncar_em_frase(trecho, 900))

    justificativa = limpar_markdown((analise or {}).get("justificativa", ""))
    if justificativa and len(justificativa) > 20:
        partes.append(f"Parecer técnico: {justificativa}")

    passos = extrair_passos_plano(plano_acao or "")
    if passos:
        prioridade = _formatar_prioridade(passos[0])
        if prioridade:
            partes.append(f"Prioridade imediata: {prioridade}")

    return "\n\n".join(partes)


def extrair_proximo_passo(resultado) -> str:
    from ui.export_utils import extrair_passos_plano

    passos = extrair_passos_plano(getattr(resultado, "plano_acao", "") or "")
    if passos:
        candidato = _formatar_prioridade(passos[0])
        if candidato and not contem_erro_tecnico(candidato):
            return truncar_em_frase(candidato, 320)

    analise = getattr(resultado, "analise", None) or {}
    resumo = limpar_markdown(analise.get("resumo", ""))
    if resumo and not contem_erro_tecnico(resumo):
        return truncar_em_frase(resumo, 320)

    return ""


def escapar_html(texto: str) -> str:
    return html.escape(limpar_markdown(texto), quote=True)


def extrair_destaques(
    texto: str,
    max_itens: int = 5,
    max_chars_item: int = 160,
    max_paragrafos: int = 1,
) -> dict[str, list[str] | str]:
    """
    Resume texto longo para UI objetiva: 1 parágrafo curto + poucos bullets.
    """
    texto = sanitizar_para_exibicao(texto or "")
    if not texto:
        return {"resumo": "", "itens": []}

    paragrafos: list[str] = []
    itens: list[str] = []
    for linha in texto.split("\n"):
        s = linha.strip()
        if not s:
            continue
        if s.startswith("- ") or re.match(r"^\d+[\.\)]\s+", s) or re.match(
            r"^passo\s+\d+", s, re.I
        ):
            item = re.sub(r"^(passo\s+\d+\s*[—\-–:]?\s*)", "", s, flags=re.I)
            item = re.sub(r"^\d+[\.\)]\s+", "", item)
            item = item.lstrip("- ").strip()
            if item and len(item) > 8:
                itens.append(truncar_em_frase(item, max_chars_item))
            continue
        if s.endswith(":") and len(s) < 80:
            continue
        if len(s) > 40:
            paragrafos.append(s)

    resumo = ""
    if paragrafos:
        resumo = truncar_em_frase(paragrafos[0], 320)
        if max_paragrafos > 1 and len(paragrafos) > 1:
            extra = truncar_em_frase(paragrafos[1], 220)
            if extra:
                resumo = f"{resumo} {extra}".strip()

    if not itens and resumo:
        # Sem bullets: quebra o resumo em frases curtas como destaques
        frases = re.split(r"(?<=[.!?])\s+", resumo)
        itens = [truncar_em_frase(f, max_chars_item) for f in frases if len(f) > 20][
            :max_itens
        ]

    return {"resumo": resumo, "itens": itens[:max_itens]}
