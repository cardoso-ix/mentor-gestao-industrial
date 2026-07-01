"""Componentes visuais do fluxo principal (passos, progresso)."""

from __future__ import annotations

import streamlit as st

from ui.timeline import renderizar_timeline_compacta


def renderizar_passos_wizard(tipo_selecionado: str) -> None:
    """Indicador horizontal das 3 etapas do wizard."""
    if tipo_selecionado:
        estados = ("done", "active", "active")
    else:
        estados = ("active", "pending", "pending")

    labels = ("Tipo de situação", "Detalhes", "Contexto da equipe")
    partes = ['<div class="fluxo-passos" role="list">']
    for i, (estado, label) in enumerate(zip(estados, labels), start=1):
        partes.append(
            f'<div class="fluxo-passo fluxo-passo--{estado}" role="listitem">'
            f'<span class="fluxo-passo__num">{i}</span>'
            f'<span class="fluxo-passo__label">{label}</span></div>'
        )
    partes.append("</div>")
    st.markdown("".join(partes), unsafe_allow_html=True)


def renderizar_painel_analise(percentual: float, etapa: str) -> None:
    """Painel de progresso na área principal durante a análise."""
    pct = int(min(max(percentual, 0), 1) * 100)
    etapa_txt = etapa or "Iniciando análise..."
    st.markdown(
        '<div class="progresso-painel" role="status" aria-live="polite" aria-busy="true">'
        '<p class="progresso-painel__titulo">Gerando orientação</p>'
        f'<p class="progresso-painel__etapa">{etapa_txt}</p>'
        f'<p class="progresso-painel__pct">{pct}% concluído</p>'
        "</div>",
        unsafe_allow_html=True,
    )
    st.progress(percentual, text=etapa_txt)
    renderizar_timeline_compacta(percentual, etapa)


def renderizar_alerta(tipo: str, mensagem: str) -> None:
    """Alertas visuais consistentes (erro, aviso, info)."""
    classes = {
        "erro": "alerta alerta--erro",
        "aviso": "alerta alerta--aviso",
        "info": "alerta alerta--info",
    }
    classe = classes.get(tipo, "alerta alerta--info")
    st.markdown(f'<div class="{classe}">{mensagem}</div>', unsafe_allow_html=True)
