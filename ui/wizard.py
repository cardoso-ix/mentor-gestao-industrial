"""
Wizard — coleta guiada de contexto por tipo de problema.
"""

from __future__ import annotations

import streamlit as st

from ui.fluxo import renderizar_passos_wizard

TIPOS_PROBLEMA = {
    "lideranca": {"label": "Liderança", "icone": "👔", "desc": "Autoridade, motivação, transição técnico→gestor"},
    "comunicacao": {"label": "Comunicação", "icone": "💬", "desc": "Alinhamento, feedback, informação"},
    "conflito": {"label": "Conflito", "icone": "⚡", "desc": "Desentendimentos, resistência, atrito"},
    "desempenho": {"label": "Desempenho", "icone": "📊", "desc": "Produtividade, qualidade, cumprimento"},
    "processo": {"label": "Processo", "icone": "⚙️", "desc": "OS, PCM, procedimentos, fluxos"},
    "seguranca": {"label": "Segurança", "icone": "🦺", "desc": "EPI, NR, lockout, permissão de trabalho"},
}

PERGUNTAS_POR_TIPO = {
    "lideranca": [
        ("Quem está envolvido?", "envolvidos"),
        ("O que você já tentou?", "tentativas"),
        ("Qual o impacto na equipe?", "impacto"),
    ],
    "comunicacao": [
        ("Qual informação não está chegando?", "info_faltando"),
        ("Quem precisa se alinhar?", "envolvidos"),
        ("O que acontece quando você tenta comunicar?", "tentativas"),
    ],
    "conflito": [
        ("Quem são as partes do conflito?", "envolvidos"),
        ("Desde quando isso ocorre?", "duracao"),
        ("O que já foi tentado?", "tentativas"),
    ],
    "desempenho": [
        ("Qual comportamento específico preocupa?", "comportamento"),
        ("Há mudança recente (cargo, turno, equipe)?", "contexto"),
        ("Qual o impacto operacional?", "impacto"),
    ],
    "processo": [
        ("Qual procedimento não está sendo seguido?", "procedimento"),
        ("Por que a equipe resiste?", "motivo"),
        ("Qual o risco operacional?", "impacto"),
    ],
    "seguranca": [
        ("Qual norma ou regra está em risco?", "norma"),
        ("O que o colaborador alega?", "motivo"),
        ("Houve incidente ou quase-acidente?", "incidente"),
    ],
}


def _inicializar_wizard():
    """Inicializa estado do wizard."""
    defaults = {
        "tipo_wizard": "",
        "situacao_wizard": "",
        "tamanho_wizard": "",
        "urgencia_wizard": "",
        "wizard_respostas": {},
        "modo_wizard": True,
    }
    for chave, valor in defaults.items():
        if chave not in st.session_state:
            st.session_state[chave] = valor


def renderizar_selecao_tipo() -> str:
    """Renderiza grid de seleção do tipo de problema. Retorna tipo selecionado."""
    st.markdown('<p class="wizard-secao-titulo">Tipo de situação</p>', unsafe_allow_html=True)
    cols = st.columns(3)
    tipo_atual = st.session_state.get("tipo_wizard", "")

    for idx, (tipo_id, info) in enumerate(TIPOS_PROBLEMA.items()):
        with cols[idx % 3]:
            selecionado = tipo_atual == tipo_id
            tipo_btn = "primary" if selecionado else "secondary"
            if st.button(
                f"{info['icone']} {info['label']}",
                key=f"tipo_{tipo_id}",
                use_container_width=True,
                type=tipo_btn,
            ):
                st.session_state.tipo_wizard = tipo_id
                st.session_state.wizard_respostas = {}
                st.rerun()

    if tipo_atual and tipo_atual in TIPOS_PROBLEMA:
        st.markdown(
            f'<div class="wizard-tipo-desc">{TIPOS_PROBLEMA[tipo_atual]["desc"]}</div>',
            unsafe_allow_html=True,
        )

    return tipo_atual


def renderizar_perguntas_guiadas(tipo: str) -> dict[str, str]:
    """Renderiza perguntas do wizard para o tipo selecionado."""
    if not tipo or tipo not in PERGUNTAS_POR_TIPO:
        return {}

    st.markdown('<p class="wizard-secao-titulo">Detalhes importantes</p>', unsafe_allow_html=True)
    respostas = dict(st.session_state.get("wizard_respostas", {}))

    for pergunta, chave in PERGUNTAS_POR_TIPO[tipo]:
        respostas[chave] = st.text_input(
            pergunta,
            value=respostas.get(chave, ""),
            key=f"wizard_{tipo}_{chave}",
        )

    st.session_state.wizard_respostas = respostas
    return respostas


def montar_situacao_do_wizard(tipo: str, respostas: dict[str, str], situacao_livre: str) -> str:
    """Monta texto final da situação combinando wizard + texto livre."""
    partes = []

    if tipo and tipo in TIPOS_PROBLEMA:
        info = TIPOS_PROBLEMA[tipo]
        partes.append(f"[Tipo: {info['label']}]")

    if situacao_livre.strip():
        partes.append(situacao_livre.strip())

    for chave, valor in respostas.items():
        if valor and valor.strip():
            label = chave.replace("_", " ").capitalize()
            partes.append(f"{label}: {valor.strip()}")

    return "\n\n".join(partes)


def renderizar_formulario_contexto() -> tuple[str, str, str]:
    """Renderiza campos de equipe, urgência e descrição livre."""
    st.markdown('<p class="wizard-secao-titulo">Contexto da equipe</p>', unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        tamanho = st.selectbox(
            "Tamanho da equipe",
            ["", "2-5 técnicos", "6-10 técnicos", "11-20 técnicos", "Mais de 20"],
            index=_indice_select(
                ["", "2-5 técnicos", "6-10 técnicos", "11-20 técnicos", "Mais de 20"],
                st.session_state.get("tamanho_wizard", ""),
            ),
            key="select_tamanho",
        )
    with col2:
        urgencia = st.selectbox(
            "Urgência",
            ["", "Baixa — posso esperar", "Média — resolver esta semana", "Alta — preciso agir hoje"],
            index=_indice_select(
                ["", "Baixa — posso esperar", "Média — resolver esta semana", "Alta — preciso agir hoje"],
                st.session_state.get("urgencia_wizard", ""),
            ),
            key="select_urgencia",
        )

    situacao_livre = st.text_area(
        "Descreva o que está acontecendo",
        value=st.session_state.get("situacao_wizard", ""),
        height=140,
        placeholder="Quem está envolvido, o que já foi tentado e qual resultado você espera...",
        key=f"situacao_wizard_{st.session_state.get('form_key', 0)}",
    )

    return tamanho, urgencia, situacao_livre


def _indice_select(opcoes: list[str], valor: str) -> int:
    """Retorna índice da opção na lista ou 0."""
    try:
        return opcoes.index(valor)
    except ValueError:
        return 0


def renderizar_wizard() -> dict | None:
    """
    Renderiza wizard completo.

    Returns:
        Dict com dados do formulário se usuário clicar em analisar, senão None.
    """
    _inicializar_wizard()

    st.markdown('<div class="wizard-panel-marker" aria-hidden="true"></div>', unsafe_allow_html=True)
    with st.container(border=True):
        renderizar_passos_wizard(st.session_state.get("tipo_wizard", ""))

        tipo = renderizar_selecao_tipo()
        if not tipo:
            st.markdown(
                '<div class="wizard-hint">Selecione um tipo de situação acima para liberar as perguntas guiadas.</div>',
                unsafe_allow_html=True,
            )
        respostas = renderizar_perguntas_guiadas(tipo) if tipo else {}
        tamanho, urgencia, situacao_livre = renderizar_formulario_contexto()

        situacao_final = montar_situacao_do_wizard(tipo, respostas, situacao_livre)

        col1, col2, col3 = st.columns([1, 1, 2])
        with col1:
            analisar = st.button("Gerar orientação", type="primary", use_container_width=True)
        with col2:
            if st.button("Limpar formulário", use_container_width=True):
                _limpar_wizard()
                st.rerun()

        if analisar:
            if not situacao_final.strip():
                st.warning("Descreva a situação antes de continuar.")
                return None
            return {
                "situacao": situacao_final,
                "tamanho_equipe": tamanho,
                "urgencia": urgencia,
                "tipo_hint": tipo,
                "categoria_rag": _mapa_categoria_rag(tipo),
            }
    return None


def _mapa_categoria_rag(tipo: str) -> str:
    """Mapeia tipo de problema para categoria da base de conhecimento."""
    mapa = {
        "seguranca": "normas",
        "processo": "processos",
        "lideranca": "gestao",
        "comunicacao": "gestao",
        "conflito": "gestao",
        "desempenho": "gestao",
    }
    return mapa.get(tipo, "")


def _limpar_wizard():
    """Limpa estado do wizard e resultado."""
    st.session_state.resultado = None
    st.session_state.form_key = st.session_state.get("form_key", 0) + 1
    st.session_state.tipo_wizard = ""
    st.session_state.situacao_wizard = ""
    st.session_state.tamanho_wizard = ""
    st.session_state.urgencia_wizard = ""
    st.session_state.wizard_respostas = {}
    st.session_state.playbook_ativo = ""
    st.session_state.checklist_plano = {}
