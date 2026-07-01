"""Rate limit simples por sessão para uso público."""

from __future__ import annotations

import time

import streamlit as st

LIMITE_ANALISES = 10
JANELA_SEGUNDOS = 3600  # 1 hora


def _inicializar():
    if "analises_timestamps" not in st.session_state:
        st.session_state.analises_timestamps = []


def pode_analisar() -> tuple[bool, str]:
    """
    Verifica se o usuário pode fazer nova análise.

    Returns:
        (permitido, mensagem)
    """
    _inicializar()
    agora = time.time()
    timestamps = [
        t for t in st.session_state.analises_timestamps
        if agora - t < JANELA_SEGUNDOS
    ]
    st.session_state.analises_timestamps = timestamps

    if len(timestamps) >= LIMITE_ANALISES:
        return False, (
            f"Limite de {LIMITE_ANALISES} análises por hora atingido. "
            "Aguarde alguns minutos e tente novamente."
        )
    return True, ""


def registrar_analise():
    """Registra timestamp de uma análise concluída."""
    _inicializar()
    st.session_state.analises_timestamps.append(time.time())
