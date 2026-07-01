"""
Playbooks — situações modelo clicáveis para preencher o formulário rapidamente.
"""

from __future__ import annotations

from dataclasses import dataclass

import streamlit as st


@dataclass
class Playbook:
    """Situação modelo pré-definida."""

    id: str
    titulo: str
    icone: str
    tipo: str
    situacao: str
    tamanho_equipe: str
    urgencia: str


PLAYBOOKS: list[Playbook] = [
    Playbook(
        id="epi",
        titulo="Técnico recusa usar EPI",
        icone="🦺",
        tipo="seguranca",
        situacao=(
            "Um técnico experiente se recusa a usar EPI obrigatório durante intervenções "
            "e está influenciando colegas a fazer o mesmo. Já conversei informalmente "
            "mas a situação persiste."
        ),
        tamanho_equipe="6-10 técnicos",
        urgencia="Alta — preciso agir hoje",
    ),
    Playbook(
        id="os",
        titulo="Resistência ao preencher OS",
        icone="📋",
        tipo="processo",
        situacao=(
            "Técnico sênior de manutenção elétrica não preenche ordem de serviço após "
            "intervenções. Diz que é perda de tempo. Outros técnicos copiam o comportamento."
        ),
        tamanho_equipe="6-10 técnicos",
        urgencia="Média — resolver esta semana",
    ),
    Playbook(
        id="turno",
        titulo="Conflito entre turnos",
        icone="🔄",
        tipo="conflito",
        situacao=(
            "Turno A acusa o Turno B de deixar equipamentos em mau estado. Reuniões de "
            "passagem de turno viraram discussões. Produtividade caiu."
        ),
        tamanho_equipe="11-20 técnicos",
        urgencia="Média — resolver esta semana",
    ),
    Playbook(
        id="pcm",
        titulo="Resistência a novo PCM",
        icone="⚙️",
        tipo="processo",
        situacao=(
            "Implementamos novo procedimento de PCM e um técnico veterano diz que o antigo "
            "funcionava melhor. Metade da equipe segue, metade resiste."
        ),
        tamanho_equipe="6-10 técnicos",
        urgencia="Baixa — posso esperar",
    ),
    Playbook(
        id="desmotivado",
        titulo="Técnico competente desmotivado",
        icone="📉",
        tipo="desempenho",
        situacao=(
            "Meu melhor técnico de instrumentação está entregando o mínimo, chegando no "
            "limite do horário e evitando assumir chamados complexos. Antes era referência."
        ),
        tamanho_equipe="2-5 técnicos",
        urgencia="Média — resolver esta semana",
    ),
]


def renderizar_playbooks_sidebar() -> Playbook | None:
    """
    Renderiza playbooks na sidebar.

    Returns:
        Playbook selecionado ou None.
    """
    st.markdown("#### Casos modelo")
    st.caption("Clique para carregar um exemplo")

    selecionado = None
    for pb in PLAYBOOKS:
        if st.button(
            f"{pb.icone} {pb.titulo}",
            key=f"playbook_{pb.id}",
            use_container_width=True,
        ):
            st.session_state.playbook_ativo = pb.id
            st.session_state.tipo_wizard = pb.tipo
            st.session_state.situacao_wizard = pb.situacao
            st.session_state.tamanho_wizard = pb.tamanho_equipe
            st.session_state.urgencia_wizard = pb.urgencia
            st.session_state.wizard_respostas = {}
            st.rerun()

    return None


def obter_playbook_por_id(playbook_id: str) -> Playbook | None:
    """Retorna playbook pelo ID."""
    for pb in PLAYBOOKS:
        if pb.id == playbook_id:
            return pb
    return None
