"""Timeline visual do progresso dos agentes."""

from __future__ import annotations

import streamlit as st

ETAPAS = [
    ("analise", "Análise", 0.2),
    ("estrategia", "Estratégia", 0.45),
    ("comunicacao", "Conversa", 0.65),
    ("plano", "Plano", 0.8),
    ("relatorio", "Síntese", 0.95),
]


def _classe_etapa(percentual: float, etapa_atual: str, etapa_id: str, limiar: float) -> tuple[str, str]:
    if percentual >= limiar:
        return "timeline-done", "✓"
    if etapa_atual and etapa_id in etapa_atual.lower():
        return "timeline-active", "●"
    return "timeline-pending", "○"


def renderizar_timeline(percentual: float, etapa_atual: str = ""):
    """Timeline vertical para a sidebar."""
    html_parts = ['<div class="timeline-vertical">']
    for etapa_id, nome, limiar in ETAPAS:
        classe, icone = _classe_etapa(percentual, etapa_atual, etapa_id, limiar)
        html_parts.append(f'<div class="timeline-step {classe}">{icone} {nome}</div>')
    html_parts.append("</div>")
    st.markdown("".join(html_parts), unsafe_allow_html=True)


def renderizar_timeline_compacta(percentual: float, etapa_atual: str = ""):
    """Timeline horizontal para a área principal."""
    html_parts = ['<div class="timeline-horizontal">']
    for etapa_id, nome, limiar in ETAPAS:
        classe, icone = _classe_etapa(percentual, etapa_atual, etapa_id, limiar)
        html_parts.append(
            f'<div class="timeline-h-item {classe}">'
            f'<span class="timeline-h-icon">{icone}</span>'
            f'<span class="timeline-h-label">{nome}</span></div>'
        )
    html_parts.append("</div>")
    st.markdown("".join(html_parts), unsafe_allow_html=True)
