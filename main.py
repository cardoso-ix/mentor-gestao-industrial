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

from ui.playbooks import renderizar_playbooks_sidebar
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
        "playbook_ativo": "",
    }
    for chave, valor in defaults.items():
        if chave not in st.session_state:
            st.session_state[chave] = valor


def _renderizar_hero():
    """Hero full-bleed: marca dominante + proposta clara."""
    st.markdown(
        '<section class="hero-bleed" aria-label="Apresentação">'
        '<div class="hero-glow" aria-hidden="true"></div>'
        '<div class="hero-grid" aria-hidden="true"></div>'
        '<div class="hero-inner">'
        '<div class="hero-copy">'
        '<p class="hero-kicker">Mentoria para supervisão industrial</p>'
        '<h1 class="hero-brand">Mentor de Gestão Industrial</h1>'
        '<p class="hero-lede">Orientação objetiva para conduzir liderança, '
        "segurança e desempenho no chão de fábrica — com diagnóstico, "
        "conversa e plano acionável.</p>"
        '<p class="hero-cta-hint">Descreva a situação abaixo</p>'
        "</div>"
        '<div class="hero-aside" aria-label="O que você recebe">'
        '<p class="hero-aside__label">Entrega</p>'
        '<span class="hero-aside__item">Diagnóstico</span>'
        '<span class="hero-aside__item">Roteiro de conversa</span>'
        '<span class="hero-aside__item">Plano de ação</span>'
        "</div>"
        "</div>"
        "</section>",
        unsafe_allow_html=True,
    )


def _renderizar_nota_geral():
    """Nota editorial do produto — caracterização profissional, sem card de marketing."""
    st.markdown(
        '<aside class="nota-geral" aria-label="Nota do produto">'
        '<p class="nota-geral__rotulo">Nota geral</p>'
        '<p class="nota-geral__texto">'
        "<strong>Ferramenta de apoio à decisão</strong> para supervisores de manutenção. "
        "Use fatos concretos do seu caso (turno, OS, nomes, o que já tentou). "
        "A orientação é um briefing executivo — adapte prazos e tom ao contexto da planta; "
        "não substitui norma interna, NR aplicável nem procedimento oficial."
        "</p>"
        "</aside>",
        unsafe_allow_html=True,
    )


def _renderizar_sidebar():
    """Barra lateral com identidade, progresso e casos modelo."""
    with st.sidebar:
        st.markdown(
            '<div class="sidebar-brand">'
            '<p class="sidebar-brand__nome">Mentor Industrial</p>'
            '<p class="sidebar-brand__desc">Apoio à supervisão de manutenção</p>'
            "</div>",
            unsafe_allow_html=True,
        )
        st.markdown("### Andamento")
        renderizar_timeline(
            st.session_state.get("timeline_pct", 0),
            st.session_state.get("timeline_etapa", ""),
        )
        st.divider()
        renderizar_playbooks_sidebar()
        st.divider()
        st.markdown(
            '<div class="aviso-publico">'
            "<strong>Uso público</strong> — limite de 10 análises por hora. "
            "Ideal para demo e casos reais curtos."
            "</div>",
            unsafe_allow_html=True,
        )


def _renderizar_rodape():
    """Rodapé com caracterização profissional."""
    ano = datetime.now().year
    st.markdown(
        '<footer class="rodape-app">'
        '<div class="rodape-app__inner">'
        '<p class="rodape-app__linha">'
        f"© {ano} Eduardo Cardoso · Mentor de Gestão Industrial"
        "</p>"
        '<p class="rodape-app__linha rodape-app__linha--muted">'
        "Briefing para supervisores de manutenção · Diagnóstico · Conversa · Plano"
        "</p>"
        "</div>"
        "</footer>",
        unsafe_allow_html=True,
    )


def main():
    """Função principal."""
    _inicializar_sessao()
    injetar_estilos()
    _renderizar_sidebar()
    _renderizar_hero()
    _renderizar_nota_geral()

    if not config.llm_configurado():
        if config.LLM_PROVIDER == "opencode_go":
            st.error(
                "Chave do OpenCode Go não configurada. Defina `OPENCODE_GO_API_KEY` "
                "no arquivo `.env` ou nos secrets do Hugging Face / Streamlit Cloud."
            )
        else:
            st.error(
                "Chave da OpenRouter não configurada. Defina `OPENROUTER_API_KEY` no "
                "arquivo `.env` ou nos secrets do Hugging Face / Streamlit Cloud."
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
        st.markdown('<div class="secao-resultado-sep" aria-hidden="true"></div>', unsafe_allow_html=True)
        renderizar_resultado(st.session_state.resultado)

    _renderizar_rodape()


if __name__ == "__main__":
    main()
