"""
Interface Streamlit do Mentor Virtual de Gestão Industrial.
"""

import streamlit as st

st.set_page_config(
    page_title="Mentor de Gestão Industrial",
    page_icon="🏭",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        "Get help": None,
        "Report a bug": None,
        "About": (
            "Mentor de Gestão Industrial — apoio a supervisores de manutenção. "
            "© Eduardo Cardoso."
        ),
    },
)

from datetime import datetime

import config

config.refresh_secrets()

from ui.rate_limit import pode_analisar, registrar_analise
from ui.fluxo import renderizar_painel_analise
from ui.resultado import renderizar_resultado
from ui.styles import injetar_estilos
from ui.timeline import renderizar_timeline
from ui.wizard import renderizar_wizard


def _inicializar_sessao():
    """Inicializa variáveis de sessão."""
    defaults = {
        "resultado": None,
        "form_key": 0,
        "timeline_pct": 0.0,
        "timeline_etapa": "",
    }
    for chave, valor in defaults.items():
        if chave not in st.session_state:
            st.session_state[chave] = valor


def _renderizar_hero():
    """Renderiza seção hero no topo da página."""
    st.markdown(
        '<div class="hero-container">'
        '<p class="hero-eyebrow">Ferramenta de apoio · Manutenção industrial</p>'
        '<h1 class="hero-title">Mentor de Gestão Industrial</h1>'
        '<p class="hero-subtitle">Diagnóstico estruturado, roteiro de conversa e plano de ação '
        "para supervisores que precisam decidir com clareza no chão de fábrica.</p>"
        "</div>",
        unsafe_allow_html=True,
    )


def _renderizar_sidebar():
    """Barra lateral com progresso da análise."""
    with st.sidebar:
        st.markdown("### Andamento")
        renderizar_timeline(
            st.session_state.get("timeline_pct", 0),
            st.session_state.get("timeline_etapa", ""),
        )
        st.divider()
        st.markdown(
            '<div class="aviso-publico">Uso público — limite de 10 análises por hora.</div>',
            unsafe_allow_html=True,
        )


def _renderizar_rodape():
    """Rodapé com direitos autorais."""
    ano = datetime.now().year
    st.markdown(
        '<footer class="rodape-app">'
        f'<p class="rodape-copy">© {ano} Eduardo Cardoso — Todos os direitos reservados.</p>'
        "</footer>",
        unsafe_allow_html=True,
    )


def main():
    """Função principal."""
    _inicializar_sessao()
    injetar_estilos()
    _renderizar_sidebar()
    _renderizar_hero()

    if not config.GROQ_API_KEY or config.GROQ_API_KEY == "sua_chave_groq_aqui":
        st.error(
            "Chave da Groq não configurada. Defina `GROQ_API_KEY` no arquivo `.env` "
            "ou nos secrets do Hugging Face / Streamlit Cloud."
        )
        return

    dados = renderizar_wizard()

    if dados and dados["situacao"].strip():
        permitido, msg_limite = pode_analisar()
        if not permitido:
            st.warning(msg_limite)
            return

        placeholder_progresso = st.empty()

        def atualizar_progresso(etapa: str, percentual: float):
            st.session_state.timeline_pct = percentual
            st.session_state.timeline_etapa = etapa
            with placeholder_progresso.container():
                renderizar_painel_analise(percentual, etapa)

        with placeholder_progresso.container():
            renderizar_painel_analise(0.0, "Iniciando análise...")

        from orchestrator import executar_mentoria

        resultado = executar_mentoria(
            situacao=dados["situacao"],
            tamanho_equipe=dados.get("tamanho_equipe", ""),
            urgencia=dados.get("urgencia", ""),
            categoria_rag=dados.get("categoria_rag", ""),
            callback_progresso=atualizar_progresso,
        )

        if not resultado.erro:
            registrar_analise()

        st.session_state.resultado = resultado
        st.session_state.timeline_pct = 1.0
        placeholder_progresso.empty()

    if st.session_state.resultado:
        st.divider()
        renderizar_resultado(st.session_state.resultado)

    _renderizar_rodape()


if __name__ == "__main__":
    main()
