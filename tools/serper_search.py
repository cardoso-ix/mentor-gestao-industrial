"""
Ferramenta de busca na web via API Serper.

Usada quando o Analista classifica o problema como 'processo' ou 'seguranca',
para complementar a base de conhecimento com informações atualizadas (normas, NR, etc.).
"""

from __future__ import annotations

import requests

import config


def buscar_web_serper(query: str, num_resultados: int = 5) -> str:
    """
    Realiza uma busca na web usando a API Serper (Google Search).

    Args:
        query: Termo ou pergunta de busca.
        num_resultados: Quantidade máxima de resultados a retornar.

    Returns:
        Texto formatado com os resultados, ou mensagem de erro/aviso.
    """
    if not config.SERPER_API_KEY:
        return "Busca web indisponível: SERPER_API_KEY não configurada."

    if not query.strip():
        return "Busca web: query vazia."

    try:
        resposta = requests.post(
            "https://google.serper.dev/search",
            headers={
                "X-API-KEY": config.SERPER_API_KEY,
                "Content-Type": "application/json",
            },
            json={"q": query, "num": num_resultados, "gl": "br", "hl": "pt-br"},
            timeout=15,
        )
        resposta.raise_for_status()
        dados = resposta.json()
    except requests.RequestException as exc:
        return f"Erro na busca web: {exc}"

    organicos = dados.get("organic", [])
    if not organicos:
        return "Nenhum resultado encontrado na busca web."

    linhas = ["## Resultados da busca web\n"]
    for item in organicos[:num_resultados]:
        titulo = item.get("title", "Sem título")
        snippet = item.get("snippet", "")
        link = item.get("link", "")
        linhas.append(f"### {titulo}\n{snippet}\nFonte: {link}\n")

    # Inclui answer box / knowledge graph se existir
    answer_box = dados.get("answerBox")
    if answer_box:
        resposta_direta = answer_box.get("answer") or answer_box.get("snippet", "")
        if resposta_direta:
            linhas.insert(1, f"**Resposta direta:** {resposta_direta}\n")

    return "\n".join(linhas)


def montar_query_busca(situacao: str, tipo_problema: str) -> str:
    """
    Monta uma query de busca otimizada para problemas de processo ou segurança.

    Args:
        situacao: Descrição da situação pelo usuário.
        tipo_problema: 'processo' ou 'seguranca'.

    Returns:
        Query formatada para a API Serper.
    """
    contexto = "manutenção industrial"
    if tipo_problema == "seguranca":
        sufixo = "norma NR segurança trabalho procedimento"
    else:
        sufixo = "procedimento manutenção industrial PCM boas práticas"

    # Limita o tamanho da query para evitar requests muito longos
    situacao_resumida = situacao[:300]
    return f"{situacao_resumida} {contexto} {sufixo}"
