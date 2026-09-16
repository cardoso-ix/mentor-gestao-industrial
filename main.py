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
    """Hero full-bleed de comando industrial moderno."""
    modelo_atual = config.OPENCODE_GO_MODEL
    st.markdown(
        f"""
        <section class="hero-bleed" aria-label="Apresentação">
            <div class="hero-glow" aria-hidden="true"></div>
            <div class="hero-grid" aria-hidden="true"></div>
            <div class="hero-inner">
                <div class="hero-copy">
                    <div class="hero-badge">
                        <span class="hero-badge__dot"></span>
                        <span>MOTOR: {modelo_atual.upper()} // OPENCODE GO</span>
                    </div>
                    <p class="hero-kicker">CENTRO DE INTELIGÊNCIA EM SUPERVISÃO</p>
                    <h1 class="hero-brand">Mentor de Gestão Industrial</h1>
                    <p class="hero-lede">
                        Inteligência artificial multi-agente para <strong>supervisores e líderes de manutenção</strong>.
                        Transforme atritos de turno, recusa de OS/EPI e baixa produtividade em diagnóstico executivo, roteiro SBI de diálogo e plano de ação imediato.
                    </p>
                    <div class="hero-quick-chips">
                        <span class="hero-quick-chip">⚡ Diagnóstico RAG</span>
                        <span class="hero-quick-chip">💬 Roteiro SBI</span>
                        <span class="hero-quick-chip">⏱️ Ação Prioritária 24h</span>
                        <span class="hero-quick-chip">📥 Briefing PDF</span>
                    </div>
                </div>
                <div class="hero-aside" aria-label="O que você recebe">
                    <p class="hero-aside__label">PAINEL DE DECISÃO</p>
                    <div class="hero-stat-card">
                        <span class="hero-stat-card__val">24h</span>
                        <span class="hero-stat-card__desc">Prazo crítico da 1ª intervenção</span>
                    </div>
                    <div class="hero-stat-card">
                        <span class="hero-stat-card__val">SBI</span>
                        <span class="hero-stat-card__desc">Situação · Comportamento · Impacto</span>
                    </div>
                </div>
            </div>
        </section>
        """,
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
    """Barra lateral com identidade, status do OpenCode Go, seletor de modelo e playbooks."""
    with st.sidebar:
        st.markdown(
            '<div class="sidebar-brand">'
            '<p class="sidebar-brand__nome">Mentor Industrial</p>'
            '<p class="sidebar-brand__desc">Apoio à supervisão de manutenção</p>'
            "</div>",
            unsafe_allow_html=True,
        )

        # Status do provedor OpenCode Go
        conectado = config.llm_configurado()
        status_cls = "badge-status-on" if conectado else "badge-status-off"
        status_txt = "OpenCode Go Conectado" if conectado else "Aguardando OPENCODE_GO_API_KEY"
        st.markdown(
            f'<div class="status-panel {status_cls}">'
            f'<span class="status-dot"></span>'
            f'<span>{status_txt}</span>'
            f'</div>',
            unsafe_allow_html=True,
        )

        if not conectado:
            st.caption("Insira sua chave para ativar a mentoria:")
            chave_digitada = st.text_input(
                "Chave OpenCode Go",
                type="password",
                placeholder="Cole sua chave aqui...",
                key="input_chave_opencode",
                label_visibility="collapsed",
            )
            if chave_digitada and chave_digitada.strip():
                chave_limpa = chave_digitada.strip()
                config.OPENCODE_GO_API_KEY = chave_limpa
                config.LLM_API_KEY = chave_limpa
                import os

                os.environ["OPENCODE_GO_API_KEY"] = chave_limpa
                os.environ["OPENAI_API_KEY"] = chave_limpa
                st.success("Chave ativa!")
                st.rerun()

        # Painel inteligente de seleção de modelos do OpenCode Go
        with st.expander("⚙️ Modelo & Motor IA", expanded=False):
            opcoes_modelos = [m["id"] for m in config.MODELOS_OPENCODE_DISPONIVEIS]
            nomes_modelos = {m["id"]: m["nome"] for m in config.MODELOS_OPENCODE_DISPONIVEIS}

            modelo_atual = config.OPENCODE_GO_MODEL
            idx_modelo = opcoes_modelos.index(modelo_atual) if modelo_atual in opcoes_modelos else 0

            selecao = st.selectbox(
                "Modelo OpenCode Go",
                options=opcoes_modelos,
                format_func=lambda x: nomes_modelos.get(x, x),
                index=idx_modelo,
                key="seletor_modelo_llm",
            )
            if selecao != config.OPENCODE_GO_MODEL:
                config.definir_modelo_ativo(selecao)
                st.toast(f"Modelo alterado para {selecao}", icon="⚡")

            st.caption(
                "**Endpoint:** `https://opencode.ai/zen/go/v1`\n\n"
                "Compatível com todos os modelos disponíveis na assinatura OpenCode Go."
            )

        if st.button("🔄 Novo Briefing / Limpar", use_container_width=True):
            from ui.wizard import _limpar_wizard

            _limpar_wizard()
            st.rerun()

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
            "<strong>⚡ DeepSeek V4.1 Flash</strong> — alta velocidade e síntese precisa para tomada de decisão no chão de fábrica."
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
        st.warning(
            "⚠️ **Chave do OpenCode Go necessária para gerar relatórios**: "
            "Insira sua `OPENCODE_GO_API_KEY` na barra lateral à esquerda ou no arquivo `.env` para executar análises."
        )

    dados = renderizar_wizard()

    if dados and dados["situacao"].strip():
        if not config.llm_configurado():
            st.error(
                "Não foi possível iniciar a análise: adicione a sua chave `OPENCODE_GO_API_KEY` "
                "na barra lateral à esquerda ou no arquivo `.env`."
            )
            return

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
