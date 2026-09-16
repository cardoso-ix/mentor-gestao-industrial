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

    labels = ("Tipo", "Relato", "Detalhes")
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
    """Painel de telemetria multi-agente em tempo real (Agent Telemetry Radar)."""
    import config
    from ui.text_utils import escapar_html

    pct = int(min(max(percentual, 0), 1) * 100)
    etapa_txt = etapa or "Iniciando orquestração multi-agente..."
    modelo = config.OPENCODE_GO_MODEL.upper()

    st.markdown(
        f"""
        <div class="agent-telemetry-hud" role="status" aria-live="polite" aria-busy="true">
            <div class="agent-telemetry-top">
                <div class="agent-radar-title-group">
                    <span class="agent-radar-pulse"></span>
                    <h3 class="agent-radar-title">Centro de Análise Multi-Agente</h3>
                </div>
                <span class="agent-radar-engine-tag">⚡ {escapar_html(modelo)}</span>
            </div>
            <div class="agent-telemetry-step">
                <span class="agent-telemetry-step__badge">ETAPA</span>
                <span>{escapar_html(etapa_txt)}</span>
            </div>
            <div class="agent-telemetry-metrics">
                <span>ORQUESTRAÇÃO: PIPELINE EM EXECUÇÃO</span>
                <span>{pct}% PROCESSADO</span>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.progress(min(max(percentual, 0.0), 1.0))
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
