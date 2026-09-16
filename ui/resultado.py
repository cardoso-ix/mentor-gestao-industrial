"""
Renderização moderna e de alto padrão executivo do painel de resultados.
Padrão Dossiê Industrial com destaques operacionais, roteiro SBI e plano tático.
"""

from __future__ import annotations

import streamlit as st

from ui.export_utils import extrair_passos_detalhados, gerar_pdf_relatorio
from ui.i18n import rotulo_complexidade, rotulo_tipo
from ui.text_utils import (
    escapar_html,
    extrair_destaques,
    extrair_proximo_passo,
    limpar_markdown,
    montar_visao_geral_profissional,
    sanitizar_para_exibicao,
    truncar_em_frase,
)


def _renderizar_metricas(analise: dict, agentes_acionados: list[str] | None = None):
    """Barra de status executiva com pills de alta legibilidade."""
    tipo = rotulo_tipo(analise.get("tipo_problema", ""))
    complexidade = rotulo_complexidade(analise.get("complexidade", "media"))

    cor_badge_complexidade = {
        "Alta": "pill-alta",
        "Média": "pill-media",
        "Baixa": "pill-baixa",
    }.get(complexidade, "pill-media")

    agentes_str = " · ".join(
        [a.capitalize() for a in (agentes_acionados or ["Analista", "Estrategista", "Plano"])]
    )

    import config

    modelo_ativo = config.OPENCODE_GO_MODEL.upper()

    st.markdown(
        f"""
        <div class="kpi-command-deck">
            <div class="kpi-stat-chip">
                <span class="kpi-stat-chip__label">CATEGORIA DA OCORRÊNCIA</span>
                <span class="kpi-stat-chip__value">{escapar_html(tipo)}</span>
            </div>
            <div class="kpi-stat-chip">
                <span class="kpi-stat-chip__label">NÍVEL DE COMPLEXIDADE</span>
                <span class="kpi-stat-chip__pill {cor_badge_complexidade}">{escapar_html(complexidade)}</span>
            </div>
            <div class="kpi-stat-chip">
                <span class="kpi-stat-chip__label">AGENTES DE SUPORTE</span>
                <span class="kpi-stat-chip__value kpi-stat-chip__value--subtle">{escapar_html(agentes_str)}</span>
            </div>
            <div class="kpi-stat-chip">
                <span class="kpi-stat-chip__label">MOTOR DE IA</span>
                <span class="kpi-stat-chip__value kpi-stat-chip__value--accent">⚡ {escapar_html(modelo_ativo)}</span>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def _renderizar_destaques(texto: str, max_itens: int = 5, vazio: str = "Conteúdo não disponível."):
    """Mostra resumo estruturado com visual limpo."""
    dados = extrair_destaques(texto, max_itens=max_itens, max_chars_item=280)
    if dados["resumo"]:
        st.markdown(f'<div class="destaque-resumo">{escapar_html(dados["resumo"])}</div>', unsafe_allow_html=True)
    if dados["itens"]:
        for item in dados["itens"]:
            st.markdown(
                f'<div class="destaque-bullet"><span class="destaque-bullet__icon">▸</span> <span>{escapar_html(item)}</span></div>',
                unsafe_allow_html=True,
            )
    if not dados["resumo"] and not dados["itens"]:
        st.info(vazio)


def _renderizar_plano_tatico(plano_texto: str):
    """Renderiza plano de ação como cards de cronograma industrial."""
    passos = extrair_passos_detalhados(plano_texto)
    if not passos:
        _renderizar_destaques(plano_texto, vazio="Plano de ação em consolidação.")
        return

    st.markdown('<div class="plano-grid">', unsafe_allow_html=True)
    for i, passo in enumerate(passos[:6], start=1):
        titulo = passo.get("titulo") or f"Etapa {i}"
        acao = passo.get("acao") or ""
        prazo = (passo.get("prazo") or "A definir").strip()
        resp = (passo.get("responsavel") or "Supervisor").strip()

        st.markdown(
            f"""
            <div class="plano-passo-card">
                <div class="plano-passo-card__header">
                    <span class="plano-passo-card__badge">ETAPA {i:02d}</span>
                    <span class="plano-passo-card__prazo">⏱️ {escapar_html(prazo)}</span>
                </div>
                <h4 class="plano-passo-card__titulo">{escapar_html(titulo)}</h4>
                <p class="plano-passo-card__acao">{escapar_html(acao)}</p>
                <div class="plano-passo-card__footer">
                    <span class="plano-passo-card__resp">Responsável: <strong>{escapar_html(resp)}</strong></span>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )
    st.markdown('</div>', unsafe_allow_html=True)

    with st.expander("📲 Checklist de Campo (Marcar Ações Realizadas)", expanded=False):
        st.caption("Acompanhe o cumprimento das etapas durante a ronda ou turno:")
        checklist = st.session_state.setdefault("checklist_plano", {})
        for i, passo in enumerate(passos[:6], start=1):
            chave_chk = f"chk_passo_{i}"
            titulo = passo.get("titulo") or f"Etapa {i}"
            prazo = (passo.get("prazo") or "").strip()
            label = f"Etapa {i:02d} ({prazo}): {titulo}"
            concluido = st.checkbox(label, value=checklist.get(chave_chk, False), key=chave_chk)
            checklist[chave_chk] = concluido


def _renderizar_roteiro_conversa(comunicacao_texto: str):
    """Renderiza roteiro de diálogo com método SBI em blocos visuais."""
    if not comunicacao_texto:
        st.info("Roteiro de diálogo direto não requerido para esta ocorrência.")
        return

    st.markdown(
        """
        <div class="sbi-intro-box">
            <span class="sbi-intro-box__tag">METODOLOGIA RECOMENDADA</span>
            <p class="sbi-intro-box__title">Feedback Estruturado SBI (Situação · Comportamento · Impacto)</p>
            <p class="sbi-intro-box__desc">Conduza a conversa em local reservado, com fatos objetivos e sem acusações subjetivas.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # Divide por parágrafos para montar blocos limpos
    paragrafos = [p.strip() for p in comunicacao_texto.split("\n\n") if p.strip()]
    for p in paragrafos:
        if p.startswith(("#", "**")):
            st.markdown(p)
        else:
            st.markdown(
                f'<div class="sbi-dialog-card"><p class="sbi-dialog-card__text">{escapar_html(p)}</p></div>',
                unsafe_allow_html=True,
            )


def _parecer_executivo(resultado) -> str:
    parecer = sanitizar_para_exibicao(
        getattr(resultado, "relatorio_consolidado", "") or ""
    )
    if not parecer:
        parecer = montar_visao_geral_profissional(
            resultado.analise or {},
            resultado.plano_acao or "",
            resultado.estrategia or "",
        )
    return parecer


def _renderizar_exportacao(resultado):
    """Botão de download de briefing executivo."""
    try:
        pdf_bytes = gerar_pdf_relatorio(resultado)
        col1, col2 = st.columns([2, 1])
        with col1:
            st.download_button(
                "📥 Baixar Briefing Completo em PDF",
                data=pdf_bytes,
                file_name="mentor_gestao_briefing_executivo.pdf",
                mime="application/pdf",
                use_container_width=True,
                type="primary",
            )
        with col2:
            st.caption("Documento pronto para impressão ou envio à gerência de manutenção.")
    except Exception as exc:
        st.caption(f"Exportação em PDF indisponível no momento: {exc}")


def renderizar_resultado(resultado):
    """Exibe o briefing final no padrão de centro de comando industrial."""
    if resultado.erro:
        st.error(resultado.erro)
        return

    analise = resultado.analise or {}

    st.markdown('<div class="resultado-shell-marker" aria-hidden="true"></div>', unsafe_allow_html=True)
    with st.container():
        st.markdown(
            """
            <div class="executive-dossier-header">
                <div>
                    <span class="executive-dossier-tag">PARECER DE GESTÃO INDUSTRIAL</span>
                    <h2 class="executive-dossier-title">Briefing Tático de Decisão</h2>
                </div>
                <span class="executive-dossier-badge">STATUS: CONCLUÍDO</span>
            </div>
            """,
            unsafe_allow_html=True,
        )

        _renderizar_metricas(analise, getattr(resultado, "agentes_acionados", []))

        # Ação Imediata das Próximas 24 Horas
        proximo = extrair_proximo_passo(resultado)
        if proximo:
            st.markdown(
                f"""
                <div class="callout-24h">
                    <div class="callout-24h__strip"></div>
                    <div class="callout-24h__content">
                        <div class="callout-24h__header">
                            <span class="callout-24h__icon">⚠️</span>
                            <span class="callout-24h__title">AÇÃO PRIORITÁRIA DAS PRÓXIMAS 24 HORAS</span>
                        </div>
                        <p class="callout-24h__text">{escapar_html(proximo)}</p>
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )

        # Abas de navegação do parecer executivo
        abas = st.tabs([
            "📌 Síntese Executiva",
            "💬 Roteiro de Conversa (SBI)",
            "📋 Plano Tático & Prazos",
            "💡 Estratégia de Gestão",
            "📚 Base Técnica & RAG",
        ])

        with abas[0]:
            st.markdown("### Síntese do Caso & Decisão")
            parecer = _parecer_executivo(resultado)
            if parecer:
                st.markdown(parecer)
            else:
                st.info("Síntese não disponível.")

            st.divider()
            _renderizar_exportacao(resultado)

        with abas[1]:
            st.markdown("### Condução da Conversa no Chão de Fábrica")
            _renderizar_roteiro_conversa(getattr(resultado, "comunicacao", ""))

        with abas[2]:
            st.markdown("### Plano de Ação Tático")
            _renderizar_plano_tatico(getattr(resultado, "plano_acao", ""))

        with abas[3]:
            st.markdown("### Estratégia de Liderança e Gestão")
            if resultado.estrategia:
                _renderizar_destaques(resultado.estrategia, max_itens=6)
            else:
                st.info("Estratégia padrão aplicada.")

        with abas[4]:
            st.markdown("### Referências Técnicas, Normas & Contexto")
            col_rag1, col_rag2 = st.columns(2)
            with col_rag1:
                st.markdown("#### Base Interna (RAG)")
                if resultado.contexto_rag:
                    st.text_area("Trechos recuperados da base:", resultado.contexto_rag, height=200, disabled=True)
                else:
                    st.caption("Nenhum trecho de norma local foi invocado para este perfil de caso.")
            with col_rag2:
                st.markdown("#### Referências Externas (Web/Serper)")
                if resultado.contexto_web:
                    st.text_area("Busca técnica externa:", resultado.contexto_web, height=200, disabled=True)
                else:
                    st.caption("Consulta externa não necessária.")
