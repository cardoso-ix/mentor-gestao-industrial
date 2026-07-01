"""Renderização do painel de resultados."""

from __future__ import annotations

import streamlit as st

from ui.export_utils import extrair_passos_plano, gerar_pdf_relatorio
from ui.i18n import rotulo_complexidade, rotulo_tipo
from ui.styles import classe_tipo_problema, cor_tipo_problema
from ui.text_utils import (
    escapar_html,
    extrair_proximo_passo,
    formatar_em_blocos,
    limpar_markdown,
    montar_visao_geral_profissional,
    sanitizar_para_exibicao,
)


def _renderizar_metricas(analise: dict, num_agentes: int):
    tipo_raw = analise.get("tipo_problema", "")
    tipo = rotulo_tipo(tipo_raw)
    complexidade = rotulo_complexidade(analise.get("complexidade", ""))
    classe = classe_tipo_problema(tipo_raw)
    cor = cor_tipo_problema(tipo_raw)

    cols = st.columns(3)
    for col, (titulo, valor) in zip(
        cols,
        [("Tema", tipo), ("Nível", complexidade), ("Especialistas", str(num_agentes))],
    ):
        with col:
            st.markdown(
                f'<div class="metric-card {classe}" style="--metric-accent:{cor};">'
                f"<h4>{titulo}</h4><p>{valor}</p></div>",
                unsafe_allow_html=True,
            )


def _renderizar_blocos(texto: str):
    """Renderiza conteúdo dos agentes com formatação profissional."""
    blocos = formatar_em_blocos(texto)
    if not blocos:
        st.write(sanitizar_para_exibicao(texto) or "Conteúdo não disponível.")
        return

    for bloco in blocos:
        if bloco["tipo"] == "titulo":
            st.markdown(f"**{bloco['texto']}**")
        elif bloco["tipo"] == "item":
            st.markdown(f"- {bloco['texto']}")
        elif bloco["tipo"] == "paragrafo":
            for linha in bloco["texto"].split("\n"):
                if linha.strip():
                    st.write(linha.strip())


def _renderizar_checklist(plano_texto: str):
    passos = extrair_passos_plano(plano_texto)
    if not passos:
        return

    st.markdown("#### Acompanhe a execução")
    if "checklist_plano" not in st.session_state:
        st.session_state.checklist_plano = {}

    for i, passo in enumerate(passos):
        chave = f"passo_{i}"
        texto = limpar_markdown(passo)[:250]
        st.session_state.checklist_plano[chave] = st.checkbox(
            texto,
            value=st.session_state.checklist_plano.get(chave, False),
            key=f"check_{chave}_{st.session_state.get('form_key', 0)}",
        )


def _renderizar_exportacao(resultado):
    try:
        pdf_bytes = gerar_pdf_relatorio(resultado)
        st.download_button(
            "Baixar resumo em PDF",
            data=pdf_bytes,
            file_name="mentor_gestao_resumo.pdf",
            mime="application/pdf",
            use_container_width=True,
            type="primary",
        )
    except Exception as exc:
        st.caption(f"PDF indisponível: {exc}")


def renderizar_resultado(resultado):
    if resultado.erro:
        st.error(resultado.erro)
        return

    analise = resultado.analise or {}
    num_agentes = len(resultado.agentes_acionados)

    st.markdown('<div class="resultado-shell-marker" aria-hidden="true"></div>', unsafe_allow_html=True)
    with st.container(border=True):
        st.markdown(
            '<div class="resultado-shell__header">'
            '<p class="resultado-shell__titulo">Orientação gerada</p>'
            f'<span class="resultado-shell__meta">{num_agentes} especialistas consultados</span>'
            "</div>"
            '<div class="resultado-banner">Pronta para consulta e exportação.</div>',
            unsafe_allow_html=True,
        )
        _renderizar_metricas(analise, num_agentes)

        proximo = extrair_proximo_passo(resultado)
        if proximo:
            st.markdown(
                '<div class="proximo-passo-card">'
                "<strong>Prioridade nas próximas 24 horas</strong>"
                f"<p>{escapar_html(proximo)}</p></div>",
                unsafe_allow_html=True,
            )

        visao = montar_visao_geral_profissional(
            analise,
            resultado.plano_acao or "",
            resultado.estrategia or "",
        )
        with st.expander("Visão geral", expanded=True):
            for paragrafo in visao.split("\n\n"):
                if paragrafo.strip():
                    st.write(paragrafo.strip())

        _renderizar_exportacao(resultado)

    st.divider()

    col_esq, col_dir = st.columns([1, 1])

    with col_esq:
        abas_esq = st.tabs(["Diagnóstico", "Estratégia"])
        with abas_esq[0]:
            st.markdown('<p class="section-heading">Diagnóstico da situação</p>', unsafe_allow_html=True)
            st.write(limpar_markdown(analise.get("resumo", "Informação não disponível.")))
            if analise.get("justificativa"):
                st.markdown("**Fundamentação**")
                st.write(limpar_markdown(analise["justificativa"]))
        with abas_esq[1]:
            st.markdown('<p class="section-heading">Estratégia de condução</p>', unsafe_allow_html=True)
            if resultado.estrategia:
                _renderizar_blocos(resultado.estrategia)
            else:
                st.info("Não foi necessário aprofundar a estratégia neste caso.")

    with col_dir:
        abas_dir = st.tabs(["Conversa", "Plano"])
        with abas_dir[0]:
            st.markdown('<p class="section-heading">Roteiro de conversa (SBI)</p>', unsafe_allow_html=True)
            if resultado.comunicacao:
                _renderizar_blocos(resultado.comunicacao)
            else:
                st.info("Não foi necessário montar roteiro de conversa.")
        with abas_dir[1]:
            st.markdown('<p class="section-heading">Plano de ação</p>', unsafe_allow_html=True)
            if resultado.plano_acao:
                _renderizar_blocos(resultado.plano_acao)
                _renderizar_checklist(resultado.plano_acao)
            else:
                st.info("Não foi necessário gerar plano detalhado.")
