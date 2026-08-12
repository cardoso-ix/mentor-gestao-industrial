"""Renderização compacta e objetiva do painel de resultados."""

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


def _renderizar_metricas(analise: dict):
    tipo = rotulo_tipo(analise.get("tipo_problema", ""))
    complexidade = rotulo_complexidade(analise.get("complexidade", ""))

    st.markdown(
        '<div class="resultado-meta" role="group" aria-label="Resumo do caso">'
        f'<div class="resultado-meta__item"><p class="resultado-meta__label">Tema</p>'
        f'<p class="resultado-meta__value">{escapar_html(tipo)}</p></div>'
        f'<div class="resultado-meta__item"><p class="resultado-meta__label">Nível</p>'
        f'<p class="resultado-meta__value">{escapar_html(complexidade)}</p></div>'
        "</div>",
        unsafe_allow_html=True,
    )


def _renderizar_destaques(texto: str, max_itens: int = 5, vazio: str = "Conteúdo não disponível."):
    """Mostra só o essencial: resumo curto + poucos bullets."""
    dados = extrair_destaques(texto, max_itens=max_itens, max_chars_item=170)
    if dados["resumo"]:
        st.write(dados["resumo"])
    if dados["itens"]:
        for item in dados["itens"]:
            st.markdown(f"- {item}")
    if not dados["resumo"] and not dados["itens"]:
        st.write(vazio)


def _renderizar_plano_compacto(plano_texto: str):
    passos = extrair_passos_detalhados(plano_texto)
    if not passos:
        _renderizar_destaques(plano_texto, vazio="Plano não disponível.")
        return

    for i, passo in enumerate(passos[:4], start=1):
        titulo = truncar_em_frase(passo.get("titulo") or f"Passo {i}", 80)
        acao = truncar_em_frase(passo.get("acao") or "", 130)
        prazo = (passo.get("prazo") or "").strip()
        linha = f"**{i}. {titulo}**"
        if acao:
            linha += f" — {acao}"
        if prazo:
            linha += f" · _{prazo}_"
        st.markdown(linha)


def _parecer_curto(resultado) -> str:
    parecer = sanitizar_para_exibicao(
        getattr(resultado, "relatorio_consolidado", "") or ""
    )
    if not parecer:
        parecer = montar_visao_geral_profissional(
            resultado.analise or {},
            resultado.plano_acao or "",
            resultado.estrategia or "",
        )
    return truncar_em_frase(parecer.replace("\n\n", " ").replace("\n", " "), 360)


def _renderizar_exportacao(resultado):
    try:
        pdf_bytes = gerar_pdf_relatorio(resultado)
        st.download_button(
            "Baixar briefing em PDF",
            data=pdf_bytes,
            file_name="mentor_gestao_briefing.pdf",
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

    st.markdown(
        '<div class="resultado-shell-marker" aria-hidden="true"></div>',
        unsafe_allow_html=True,
    )
    with st.container(border=True):
        st.markdown(
            '<div class="resultado-shell__header">'
            '<p class="resultado-shell__titulo">Orientação pronta</p>'
            '<span class="resultado-shell__meta">Briefing executivo</span>'
            "</div>",
            unsafe_allow_html=True,
        )
        st.markdown(
            '<p class="resultado-nota">'
            "Leitura recomendada: priorize a ação das próximas 24h, "
            "use o roteiro na conversa e adapte o plano ao turno e à planta."
            "</p>",
            unsafe_allow_html=True,
        )
        _renderizar_metricas(analise)

        proximo = extrair_proximo_passo(resultado)
        if proximo:
            st.markdown(
                '<div class="proximo-passo-card">'
                "<strong>Faça nas próximas 24 horas</strong>"
                f"<p>{escapar_html(proximo)}</p></div>",
                unsafe_allow_html=True,
            )

        parecer = _parecer_curto(resultado)
        if parecer:
            st.markdown(
                '<p class="section-heading section-heading--inline">Em síntese</p>',
                unsafe_allow_html=True,
            )
            st.write(parecer)
        else:
            st.write("Parecer indisponível para este caso.")

        _renderizar_exportacao(resultado)

    abas = st.tabs(["Diagnóstico", "Estratégia", "Conversa", "Plano"])

    with abas[0]:
        st.write(
            truncar_em_frase(
                limpar_markdown(analise.get("resumo", "Informação não disponível.")),
                300,
            )
        )
        if analise.get("justificativa"):
            st.caption(
                truncar_em_frase(limpar_markdown(analise["justificativa"]), 160)
            )

    with abas[1]:
        if resultado.estrategia:
            _renderizar_destaques(resultado.estrategia)
        else:
            st.info("Estratégia não foi necessária neste caso.")

    with abas[2]:
        if resultado.comunicacao:
            _renderizar_destaques(resultado.comunicacao, max_itens=4)
        else:
            st.info("Roteiro de conversa não foi necessário neste caso.")

    with abas[3]:
        if resultado.plano_acao:
            _renderizar_plano_compacto(resultado.plano_acao)
        else:
            st.info("Plano detalhado não foi necessário neste caso.")
