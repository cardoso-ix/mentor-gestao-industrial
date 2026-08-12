"""
Wizard — coleta guiada, humanizada e de preenchimento rápido.
"""

from __future__ import annotations

import streamlit as st

from ui.fluxo import renderizar_passos_wizard
from ui.playbooks import renderizar_casos_um_clique

TIPOS_PROBLEMA = {
    "lideranca": {
        "label": "Liderança",
        "desc": "Autoridade, motivação ou transição de técnico para gestor",
        "exemplo": (
            "Meu técnico mais experiente da elétrica não aceita orientação na frente "
            "da equipe. Já conversei duas vezes e o clima no turno B piorou."
        ),
    },
    "comunicacao": {
        "label": "Comunicação",
        "desc": "Alinhamento, feedback ou informação que não chega",
        "exemplo": (
            "As passagens de turno estão incompletas. O turno seguinte perde tempo "
            "retrabalhando e a equipe reclama que ninguém avisa o status das OS."
        ),
    },
    "conflito": {
        "label": "Conflito",
        "desc": "Atrito entre pessoas ou resistência na equipe",
        "exemplo": (
            "Dois mecânicos estão em atrito desde a última parada. Um acusa o outro "
            "de deixar serviço pela metade e isso já atrasou duas intervenções."
        ),
    },
    "desempenho": {
        "label": "Desempenho",
        "desc": "Produtividade, qualidade ou tarefa que não é cumprida",
        "exemplo": (
            "Um técnico sênior se recusa a preencher a OS depois das intervenções. "
            "Diz que é perda de tempo e outros começaram a copiar."
        ),
    },
    "processo": {
        "label": "Processo",
        "desc": "OS, PCM, procedimento ou fluxo que não é seguido",
        "exemplo": (
            "A equipe pula a liberação formal antes de iniciar serviço. Já orientei "
            "no quadro, mas o padrão não pegou e o PCM perde rastreabilidade."
        ),
    },
    "seguranca": {
        "label": "Segurança",
        "desc": "EPI, NR, lockout ou permissão de trabalho",
        "exemplo": (
            "Um eletricista insiste em entrar em painel sem LOTO completo. Alega "
            "pressa da produção. Quase-acidente na semana passada."
        ),
    },
}

PERGUNTAS_POR_TIPO = {
    "lideranca": [
        ("Quem está no centro disso?", "envolvidos", "Ex.: João, técnico sênior do turno B"),
        ("O que você já tentou?", "tentativas", "Ex.: conversei 2 vezes; falei no toolbox"),
        ("Como isso afeta a equipe?", "impacto", "Ex.: outros copiam; clima ficou tenso"),
    ],
    "comunicacao": [
        ("O que não está chegando?", "info_faltando", "Ex.: status da OS na passagem de turno"),
        ("Quem precisa se alinhar?", "envolvidos", "Ex.: turnos A e B; PCM e área"),
        ("O que acontece quando você tenta alinhar?", "tentativas", "Ex.: concordam e depois voltam ao padrão"),
    ],
    "conflito": [
        ("Quem está envolvido?", "envolvidos", "Ex.: Carlos e André, mecânica"),
        ("Isso vem de quando?", "duracao", "Ex.: desde a parada do dia 12"),
        ("O que já foi tentado?", "tentativas", "Ex.: medição informal; troca de dupla"),
    ],
    "desempenho": [
        ("Qual comportamento te preocupa?", "comportamento", "Ex.: não preenche OS ao finalizar"),
        ("Teve mudança recente?", "contexto", "Ex.: novo supervisor; troca de turno"),
        ("Qual impacto na operação?", "impacto", "Ex.: perde histórico; MTTR sobe"),
    ],
    "processo": [
        ("Qual procedimento está falhando?", "procedimento", "Ex.: liberação / preenchimento de OS"),
        ("Por que a equipe evita seguir?", "motivo", "Ex.: acham burocrático; pressão de produção"),
        ("Qual risco isso gera?", "impacto", "Ex.: retrabalho; falha de rastreabilidade"),
    ],
    "seguranca": [
        ("Qual regra ou norma está em risco?", "norma", "Ex.: LOTO / NR-10 / EPI"),
        ("O que a pessoa alega?", "motivo", "Ex.: produção pressionando prazo"),
        ("Já houve incidente ou quase-acidente?", "incidente", "Ex.: sim, semana passada no painel 3"),
    ],
}

LABELS_CONTEXTO_PLANTA = {
    "planta_turno": "Onde isso acontece (área/turno)",
    "clima_equipe": "Como está o clima",
    "historico_colaborador": "Como é a pessoa envolvida",
    "indicador_meta": "O que está sendo prejudicado",
}


def _inicializar_wizard():
    """Inicializa estado do wizard."""
    defaults = {
        "tipo_wizard": "",
        "situacao_wizard": "",
        "tamanho_wizard": "",
        "urgencia_wizard": "",
        "wizard_respostas": {},
        "contexto_planta": {},
        "modo_wizard": True,
    }
    for chave, valor in defaults.items():
        if chave not in st.session_state:
            st.session_state[chave] = valor


def renderizar_selecao_tipo() -> str:
    """Renderiza grid de seleção do tipo de problema."""
    st.markdown(
        '<p class="wizard-secao-titulo">1. Tipo da situação</p>',
        unsafe_allow_html=True,
    )
    st.caption("Selecione o enquadramento mais próximo do caso.")
    cols = st.columns(3)
    tipo_atual = st.session_state.get("tipo_wizard", "")

    for idx, (tipo_id, info) in enumerate(TIPOS_PROBLEMA.items()):
        with cols[idx % 3]:
            selecionado = tipo_atual == tipo_id
            tipo_btn = "primary" if selecionado else "secondary"
            if st.button(
                info["label"],
                key=f"tipo_{tipo_id}",
                use_container_width=True,
                type=tipo_btn,
                help=info["desc"],
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
    """Perguntas opcionais, em linguagem simples."""
    if not tipo or tipo not in PERGUNTAS_POR_TIPO:
        return {}

    respostas = dict(st.session_state.get("wizard_respostas", {}))
    for pergunta, chave, placeholder in PERGUNTAS_POR_TIPO[tipo]:
        respostas[chave] = st.text_input(
            pergunta,
            value=respostas.get(chave, ""),
            placeholder=placeholder,
            key=f"wizard_{tipo}_{chave}",
        )
    st.session_state.wizard_respostas = respostas
    return respostas


def renderizar_contexto_planta() -> dict[str, str]:
    """Contexto opcional da planta, em perguntas humanas."""
    ctx = dict(st.session_state.get("contexto_planta", {}))

    col1, col2 = st.columns(2)
    with col1:
        ctx["planta_turno"] = st.text_input(
            LABELS_CONTEXTO_PLANTA["planta_turno"],
            value=ctx.get("planta_turno", ""),
            placeholder="Ex.: elétrica, turno B",
            key="ctx_planta_turno",
        )
        ctx["historico_colaborador"] = st.text_input(
            LABELS_CONTEXTO_PLANTA["historico_colaborador"],
            value=ctx.get("historico_colaborador", ""),
            placeholder="Ex.: sênior, bom tecnicamente, já orientei 2x",
            key="ctx_historico_colaborador",
        )
    with col2:
        clima_opcoes = [
            "",
            "Tranquilo",
            "Tenso",
            "Há pressão de produção",
            "Clima delicado / sindicato",
        ]
        ctx["clima_equipe"] = st.selectbox(
            LABELS_CONTEXTO_PLANTA["clima_equipe"],
            clima_opcoes,
            index=_indice_select(clima_opcoes, ctx.get("clima_equipe", "")),
            key="ctx_clima_equipe",
        )
        ctx["indicador_meta"] = st.text_input(
            LABELS_CONTEXTO_PLANTA["indicador_meta"],
            value=ctx.get("indicador_meta", ""),
            placeholder="Ex.: % OS preenchidas, MTTR, retrabalho",
            key="ctx_indicador_meta",
        )

    st.session_state.contexto_planta = ctx
    return ctx


def montar_situacao_do_wizard(
    tipo: str,
    respostas: dict[str, str],
    situacao_livre: str,
    contexto_planta: dict[str, str] | None = None,
) -> str:
    """Monta texto final da situação combinando narrativa + detalhes opcionais."""
    partes = []

    if tipo and tipo in TIPOS_PROBLEMA:
        partes.append(f"[Tipo: {TIPOS_PROBLEMA[tipo]['label']}]")

    if situacao_livre.strip():
        partes.append(situacao_livre.strip())

    for chave, valor in (contexto_planta or {}).items():
        if valor and str(valor).strip():
            label = LABELS_CONTEXTO_PLANTA.get(chave, chave.replace("_", " ").capitalize())
            partes.append(f"{label}: {str(valor).strip()}")

    labels_resposta = {
        "envolvidos": "Envolvidos",
        "tentativas": "O que já foi tentado",
        "impacto": "Impacto",
        "info_faltando": "Informação que não chega",
        "duracao": "Desde quando",
        "comportamento": "Comportamento observado",
        "contexto": "Contexto recente",
        "procedimento": "Procedimento",
        "motivo": "Motivo alegado",
        "norma": "Norma/regra",
        "incidente": "Incidente/quase-acidente",
    }
    for chave, valor in respostas.items():
        if valor and valor.strip():
            label = labels_resposta.get(chave, chave.replace("_", " ").capitalize())
            partes.append(f"{label}: {valor.strip()}")

    return "\n\n".join(partes)


def renderizar_narrativa_principal(tipo: str) -> str:
    """Campo principal: contar o caso com as próprias palavras."""
    st.markdown(
        '<p class="wizard-secao-titulo">2. Relato do caso</p>',
        unsafe_allow_html=True,
    )
    st.caption(
        "Seja concreto: nomes, OS, turno, impacto e o que já foi tentado."
    )

    placeholder = (
        TIPOS_PROBLEMA.get(tipo, {}).get("exemplo")
        or "Ex.: um técnico sênior não preenche OS e outros começaram a copiar..."
    )

    col_a, col_b = st.columns([1, 1])
    with col_a:
        if tipo and st.button("Usar um exemplo deste tipo", use_container_width=True):
            exemplo = TIPOS_PROBLEMA[tipo]["exemplo"]
            st.session_state[f"situacao_wizard_{st.session_state.get('form_key', 0)}"] = exemplo
            st.session_state.situacao_wizard = exemplo
            st.rerun()
    with col_b:
        st.caption("O exemplo só ajuda a começar — edite com o seu caso real.")

    situacao_livre = st.text_area(
        "Sua situação",
        value=st.session_state.get("situacao_wizard", ""),
        height=160,
        placeholder=placeholder,
        label_visibility="collapsed",
        key=f"situacao_wizard_{st.session_state.get('form_key', 0)}",
    )
    st.session_state.situacao_wizard = situacao_livre
    return situacao_livre


def renderizar_urgencia_equipe() -> tuple[str, str]:
    """Campos rápidos de urgência e tamanho."""
    st.markdown(
        '<p class="wizard-secao-titulo">3. Urgência e equipe</p>',
        unsafe_allow_html=True,
    )
    col1, col2 = st.columns(2)
    with col1:
        urgencia = st.selectbox(
            "Urgência",
            [
                "",
                "Baixa — posso esperar",
                "Média — resolver esta semana",
                "Alta — preciso agir hoje",
            ],
            index=_indice_select(
                [
                    "",
                    "Baixa — posso esperar",
                    "Média — resolver esta semana",
                    "Alta — preciso agir hoje",
                ],
                st.session_state.get("urgencia_wizard", ""),
            ),
            key="select_urgencia",
        )
    with col2:
        tamanho = st.selectbox(
            "Tamanho da equipe (opcional)",
            ["", "2-5 técnicos", "6-10 técnicos", "11-20 técnicos", "Mais de 20"],
            index=_indice_select(
                ["", "2-5 técnicos", "6-10 técnicos", "11-20 técnicos", "Mais de 20"],
                st.session_state.get("tamanho_wizard", ""),
            ),
            key="select_tamanho",
        )
    return tamanho, urgencia


def _indice_select(opcoes: list[str], valor: str) -> int:
    try:
        return opcoes.index(valor)
    except ValueError:
        return 0


def renderizar_wizard() -> dict | None:
    """
    Wizard humanizado: tipo → narrativa → urgência → detalhes opcionais.
    """
    _inicializar_wizard()

    st.markdown('<div class="wizard-panel-marker" aria-hidden="true"></div>', unsafe_allow_html=True)
    with st.container():
        st.markdown(
            '<div class="wizard-intro">'
            '<p class="wizard-intro__titulo">Caso da supervisão</p>'
            '<p class="wizard-intro__texto">'
            "Escolha o tipo, descreva o fato com clareza e gere um briefing para agir."
            "</p>"
            "</div>",
            unsafe_allow_html=True,
        )
        renderizar_casos_um_clique()
        st.markdown('<div class="wizard-divider" aria-hidden="true"></div>', unsafe_allow_html=True)
        renderizar_passos_wizard(st.session_state.get("tipo_wizard", ""))

        tipo = renderizar_selecao_tipo()
        if not tipo:
            st.markdown(
                '<div class="wizard-hint">Selecione o tipo da situação para começar. '
                "Em seguida, descreva o caso com fatos do turno e da planta.</div>",
                unsafe_allow_html=True,
            )

        situacao_livre = renderizar_narrativa_principal(tipo)
        tamanho, urgencia = renderizar_urgencia_equipe()

        respostas: dict[str, str] = {}
        contexto_planta: dict[str, str] = {}
        with st.expander("Detalhes opcionais (deixam a orientação mais precisa)", expanded=False):
            st.caption("Nada aqui é obrigatório. Preencha só o que souber.")
            if tipo:
                st.markdown("**Alguns detalhes do caso**")
                respostas = renderizar_perguntas_guiadas(tipo)
            st.markdown("**Contexto da planta**")
            contexto_planta = renderizar_contexto_planta()

        situacao_final = montar_situacao_do_wizard(
            tipo, respostas, situacao_livre, contexto_planta
        )

        st.markdown(
            '<div class="wizard-acoes-hint">Pronto para o briefing? Gere a orientação.</div>',
            unsafe_allow_html=True,
        )
        col1, col2, col3 = st.columns([1, 1, 2])
        with col1:
            analisar = st.button(
                "Gerar briefing",
                type="primary",
                use_container_width=True,
                disabled=not bool(tipo and situacao_livre.strip()),
            )
        with col2:
            if st.button("Limpar formulário", use_container_width=True):
                _limpar_wizard()
                st.rerun()

        if analisar:
            if not tipo:
                st.warning("Escolha o tipo da situação para continuar.")
                return None
            if not situacao_livre.strip():
                st.warning("Conte com suas palavras o que está acontecendo.")
                return None
            return {
                "situacao": situacao_final,
                "tamanho_equipe": tamanho,
                "urgencia": urgencia,
                "tipo_hint": tipo,
                "contexto_planta": contexto_planta,
                "categoria_rag": _mapa_categoria_rag(tipo),
            }
    return None


def _mapa_categoria_rag(tipo: str) -> str:
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
    st.session_state.resultado = None
    st.session_state.form_key = st.session_state.get("form_key", 0) + 1
    st.session_state.tipo_wizard = ""
    st.session_state.situacao_wizard = ""
    st.session_state.tamanho_wizard = ""
    st.session_state.urgencia_wizard = ""
    st.session_state.wizard_respostas = {}
    st.session_state.contexto_planta = {}
    st.session_state.playbook_ativo = ""
    st.session_state.checklist_plano = {}
