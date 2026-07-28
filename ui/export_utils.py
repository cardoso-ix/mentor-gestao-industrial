"""Utilitários de exportação PDF resumido com passo a passo completo."""

from __future__ import annotations

import io
import re
import unicodedata
from datetime import datetime
from typing import Any

from ui.text_utils import contem_erro_tecnico, extrair_proximo_passo, limpar_markdown, truncar_em_frase

LIMITE_RESUMO = 520
LIMITE_PROXIMO_PASSO = 280
LIMITE_PASSO_TITULO = 90
LIMITE_PASSO_ACAO = 220
MAX_PASSOS_PDF = 8
MAX_BULLETS_CONVERSA = 5


def _texto_pdf(texto: str) -> str:
    if not texto:
        return ""
    nfkd = unicodedata.normalize("NFKD", str(texto))
    sem_acento = "".join(c for c in nfkd if not unicodedata.combining(c))
    return (
        sem_acento.replace("**", "")
        .replace("###", "")
        .replace("##", "")
        .replace("#", "")
        .replace("\u2022", "-")
        .replace("\u2014", "-")
        .replace("\u2013", "-")
    )


def _truncar(texto: str, limite: int) -> str:
    if not texto:
        return ""
    texto = texto.strip()
    if len(texto) <= limite:
        return texto
    corte = texto[:limite].rsplit(" ", 1)[0]
    return (corte or texto[:limite]).rstrip(".,;:") + "..."


def _limpar_rotulo_passo(texto: str) -> str:
    t = limpar_markdown(texto or "")
    t = re.sub(r"^(Passo\s+\d+\s*[—\-–:]?\s*)", "", t, flags=re.I)
    t = re.sub(r"\s*—\s*-\s*O que fazer:\s*", ": ", t, flags=re.I)
    t = re.sub(r"\s*-\s*O que fazer:\s*", ": ", t, flags=re.I)
    return re.sub(r"\s{2,}", " ", t).strip()


def extrair_passos_detalhados(texto_plano: str) -> list[dict[str, str]]:
    """
    Extrai passos estruturados do plano de ação.

    Retorna dicts com: titulo, acao, prazo, responsavel, indicador.
    """
    if not texto_plano:
        return []

    linhas = [l.rstrip() for l in texto_plano.split("\n")]
    passos: list[dict[str, str]] = []
    atual: dict[str, str] | None = None

    def fechar():
        nonlocal atual
        if not atual:
            return
        if atual.get("titulo") or atual.get("acao"):
            passos.append(atual)
        atual = None

    for linha in linhas:
        s = linha.strip()
        if not s:
            continue

        m_passo = re.match(
            r"^(?:\*\*)?Passo\s+(\d+)\s*[—\-–:]?\s*(.+?)(?:\*\*)?$",
            s,
            re.I,
        )
        m_num = re.match(r"^(\d+)[\.\)]\s+(.+)$", s)

        if m_passo or (m_num and not s.lower().startswith("- ")):
            fechar()
            titulo_bruto = (m_passo.group(2) if m_passo else m_num.group(2)).strip()
            atual = {
                "titulo": _limpar_rotulo_passo(titulo_bruto),
                "acao": "",
                "prazo": "",
                "responsavel": "",
                "indicador": "",
            }
            continue

        if not atual:
            continue

        m_campo = re.match(
            r"^[-•]?\s*(O que fazer|Prazo sugerido|Prazo|Respons[aá]vel|Indicador de sucesso)\s*:\s*(.+)$",
            s,
            re.I,
        )
        if m_campo:
            campo = m_campo.group(1).lower()
            valor = m_campo.group(2).strip()
            if "fazer" in campo:
                atual["acao"] = valor
            elif "prazo" in campo:
                atual["prazo"] = valor
            elif "respons" in campo:
                atual["responsavel"] = valor
            elif "indicador" in campo:
                atual["indicador"] = valor
            continue

        # Linha solta após o título: usa como ação se ainda vazia
        if not atual["acao"] and not s.endswith(":"):
            atual["acao"] = limpar_markdown(s.lstrip("- ").strip())

    fechar()

    limpos = []
    for p in passos:
        if contem_erro_tecnico(p.get("titulo", "")) or contem_erro_tecnico(p.get("acao", "")):
            continue
        if not p.get("titulo") and not p.get("acao"):
            continue
        limpos.append(p)
    return limpos[:MAX_PASSOS_PDF]


def extrair_passos_plano(texto_plano: str) -> list[str]:
    """Lista simples de passos (compatível com checklist da UI)."""
    detalhados = extrair_passos_detalhados(texto_plano)
    if detalhados:
        saida = []
        for p in detalhados:
            titulo = p.get("titulo") or "Acao"
            acao = p.get("acao")
            if acao:
                saida.append(f"{titulo}: {acao}")
            else:
                saida.append(titulo)
        return saida

    # Fallback legado
    passos = []
    for linha in (texto_plano or "").split("\n"):
        linha = linha.strip()
        if re.match(r"^(\*\*)?Passo\s+\d+", linha, re.I) or re.match(r"^\d+[\.\)]\s+", linha):
            passos.append(re.sub(r"^\d+[\.\)]\s+", "", linha))
        elif linha.startswith("- O que fazer:") and passos:
            passos[-1] += f" — {linha}"
    if not passos and (texto_plano or "").strip():
        passos = [limpar_markdown(texto_plano)[:300]]
    return [p for p in passos if p and not contem_erro_tecnico(p)][:10]


def _extrair_secao(texto: str, titulos: tuple[str, ...]) -> str:
    if not texto:
        return ""
    linhas = limpar_markdown(texto).split("\n")
    capturando = False
    buffer: list[str] = []
    for linha in linhas:
        s = linha.strip()
        if not s:
            if capturando and buffer:
                break
            continue
        titulo = s[:-1].strip().lower() if s.endswith(":") else ""
        if any(titulo.startswith(t.lower()) for t in titulos):
            capturando = True
            continue
        if capturando and s.endswith(":") and len(s) < 80:
            break
        if capturando:
            buffer.append(s)
    return "\n".join(buffer).strip()


def _bullets_de_texto(texto: str, limite: int = MAX_BULLETS_CONVERSA) -> list[str]:
    if not texto:
        return []
    itens = []
    for linha in limpar_markdown(texto).split("\n"):
        s = linha.strip()
        if s.startswith("- "):
            item = s[2:].strip()
        elif re.match(r"^\d+[\.\)]\s+", s):
            item = re.sub(r"^\d+[\.\)]\s+", "", s).strip()
        else:
            continue
        if item and not contem_erro_tecnico(item) and len(item) > 12:
            itens.append(truncar_em_frase(item, 180))
        if len(itens) >= limite:
            break
    return itens


def _resumo_para_pdf(resultado) -> str:
    analise = resultado.analise or {}
    if analise.get("resumo"):
        return truncar_em_frase(limpar_markdown(analise["resumo"]), LIMITE_RESUMO)

    parecer = limpar_markdown((resultado.relatorio_consolidado or "").strip())
    secao = _extrair_secao(parecer, ("Parecer executivo", "Resumo", "Diagnostico", "Diagnóstico"))
    if secao and not contem_erro_tecnico(secao):
        return truncar_em_frase(secao, LIMITE_RESUMO)
    if parecer and not contem_erro_tecnico(parecer):
        return truncar_em_frase(parecer, LIMITE_RESUMO)
    return ""


def _formatar_passo_pdf(passo: dict[str, str], indice: int) -> tuple[str, str]:
    titulo = _truncar(passo.get("titulo") or f"Passo {indice}", LIMITE_PASSO_TITULO)
    partes = []
    if passo.get("acao"):
        partes.append(_truncar(passo["acao"], LIMITE_PASSO_ACAO))
    meta = []
    if passo.get("prazo"):
        meta.append(f"Prazo: {passo['prazo']}")
    if passo.get("responsavel"):
        meta.append(f"Responsavel: {passo['responsavel']}")
    if passo.get("indicador"):
        meta.append(f"Sucesso: {_truncar(passo['indicador'], 120)}")
    corpo = " ".join(partes)
    if meta:
        corpo = (corpo + "\n" if corpo else "") + " | ".join(meta)
    return titulo, corpo


class RelatorioPDF:
    COR_FUNDO = (255, 255, 255)
    COR_FUNDO_DESTAQUE = (255, 247, 237)
    COR_TEXTO = (12, 10, 9)
    COR_TEXTO_SECUNDARIO = (120, 113, 108)
    COR_DESTAQUE = (217, 119, 6)
    COR_BORDA = (214, 211, 209)
    COR_HEADER = (28, 25, 23)
    COR_HEADER_TEXTO = (255, 255, 255)
    COR_META = (68, 64, 60)

    MARGEM_L = 16
    MARGEM_R = 16
    ALTURA_HEADER = 26
    ALTURA_FOOTER = 14

    def __init__(self):
        from fpdf import FPDF

        self.data_geracao = datetime.now().strftime("%d/%m/%Y %H:%M")
        self.pdf = FPDF(orientation="P", unit="mm", format="A4")
        self.pdf.set_auto_page_break(auto=True, margin=self.ALTURA_FOOTER + 6)
        self.pdf.set_margins(self.MARGEM_L, self.ALTURA_HEADER + 5, self.MARGEM_R)
        self._largura_util = self.pdf.w - self.MARGEM_L - self.MARGEM_R

    def _pintar_fundo(self):
        self.pdf.set_fill_color(*self.COR_FUNDO)
        self.pdf.rect(0, 0, self.pdf.w, self.pdf.h, style="F")

    def _desenhar_cabecalho(self):
        self.pdf.set_fill_color(*self.COR_HEADER)
        self.pdf.rect(0, 0, self.pdf.w, self.ALTURA_HEADER, style="F")
        self.pdf.set_fill_color(*self.COR_DESTAQUE)
        self.pdf.rect(0, self.ALTURA_HEADER - 1.4, self.pdf.w, 1.4, style="F")

        self.pdf.set_xy(self.MARGEM_L, 6)
        self.pdf.set_font("Helvetica", "B", 12)
        self.pdf.set_text_color(*self.COR_HEADER_TEXTO)
        self.pdf.cell(0, 6, _texto_pdf("MENTOR DE GESTAO INDUSTRIAL"), ln=False)

        self.pdf.set_font("Helvetica", "", 8)
        self.pdf.set_text_color(253, 186, 116)
        self.pdf.set_xy(self.MARGEM_L, 14.5)
        self.pdf.cell(
            self._largura_util,
            4,
            _texto_pdf(f"Resumo executivo  |  {self.data_geracao}"),
            align="R",
        )
        self.pdf.set_y(self.ALTURA_HEADER + 6)

    def _desenhar_rodape(self):
        y = self.pdf.h - self.ALTURA_FOOTER
        self.pdf.set_draw_color(*self.COR_BORDA)
        self.pdf.line(self.MARGEM_L, y, self.pdf.w - self.MARGEM_R, y)
        self.pdf.set_font("Helvetica", "", 7)
        self.pdf.set_text_color(*self.COR_TEXTO_SECUNDARIO)
        self.pdf.set_xy(self.MARGEM_L, y + 3)
        self.pdf.cell(
            self._largura_util,
            4,
            _texto_pdf(
                f"(c) Eduardo Cardoso - Todos os direitos reservados  |  Pag. {self.pdf.page_no()}"
            ),
            align="C",
        )

    def _nova_pagina(self):
        self.pdf.add_page()
        self._pintar_fundo()
        self._desenhar_cabecalho()

    def _garantir_espaco(self, mm: float = 28):
        if self.pdf.get_y() > self.pdf.h - self.ALTURA_FOOTER - mm:
            self._nova_pagina()

    def _titulo_secao(self, titulo: str):
        self._garantir_espaco(30)
        y = self.pdf.get_y()
        self.pdf.set_fill_color(*self.COR_DESTAQUE)
        self.pdf.rect(self.MARGEM_L, y + 0.8, 2.2, 6, style="F")
        self.pdf.set_xy(self.MARGEM_L + 5, y)
        self.pdf.set_font("Helvetica", "B", 11)
        self.pdf.set_text_color(*self.COR_TEXTO)
        self.pdf.cell(0, 7, _texto_pdf(titulo), ln=True)
        self.pdf.ln(1.2)

    def _paragrafo(self, texto: str):
        if not texto:
            return
        self._garantir_espaco(16)
        self.pdf.set_font("Helvetica", "", 10)
        self.pdf.set_text_color(*self.COR_TEXTO)
        self.pdf.multi_cell(self._largura_util, 5.2, _texto_pdf(texto))
        self.pdf.ln(2.2)

    def _caixa_destaque(self, titulo: str, conteudo: str):
        if not conteudo:
            return
        texto = _texto_pdf(truncar_em_frase(conteudo, LIMITE_PROXIMO_PASSO))
        # estima altura
        linhas = max(2, (len(texto) // 78) + 1)
        altura = 12 + linhas * 5
        self._garantir_espaco(altura + 6)
        y0 = self.pdf.get_y()

        self.pdf.set_fill_color(*self.COR_FUNDO_DESTAQUE)
        self.pdf.set_draw_color(*self.COR_DESTAQUE)
        self.pdf.rect(self.MARGEM_L, y0, self._largura_util, altura, style="DF")
        self.pdf.set_xy(self.MARGEM_L + 4, y0 + 2.5)
        self.pdf.set_font("Helvetica", "B", 8)
        self.pdf.set_text_color(*self.COR_DESTAQUE)
        self.pdf.cell(0, 4, _texto_pdf(titulo.upper()), ln=True)
        self.pdf.set_x(self.MARGEM_L + 4)
        self.pdf.set_font("Helvetica", "", 10)
        self.pdf.set_text_color(*self.COR_TEXTO)
        self.pdf.multi_cell(self._largura_util - 8, 5, texto)
        self.pdf.set_y(y0 + altura + 3.5)

    def _lista_bullets(self, itens: list[str]):
        for item in itens:
            self._garantir_espaco(12)
            self.pdf.set_font("Helvetica", "B", 10)
            self.pdf.set_text_color(*self.COR_DESTAQUE)
            self.pdf.cell(5, 5, "-", ln=False)
            self.pdf.set_font("Helvetica", "", 10)
            self.pdf.set_text_color(*self.COR_TEXTO)
            self.pdf.multi_cell(self._largura_util - 5, 5.1, _texto_pdf(item))
            self.pdf.ln(0.8)

    def _passo_a_passo(self, passos: list[dict[str, str]]):
        if not passos:
            return
        self._titulo_secao("Passo a passo do processo")
        self.pdf.set_font("Helvetica", "", 9)
        self.pdf.set_text_color(*self.COR_TEXTO_SECUNDARIO)
        self.pdf.multi_cell(
            self._largura_util,
            4.6,
            _texto_pdf(
                "Sequencia resumida para executar a orientacao. Siga na ordem e "
                "ajuste prazos conforme a urgencia da planta."
            ),
        )
        self.pdf.ln(2)

        for i, passo in enumerate(passos, start=1):
            titulo, corpo = _formatar_passo_pdf(passo, i)
            self._garantir_espaco(22)

            # Número + título
            self.pdf.set_font("Helvetica", "B", 10)
            self.pdf.set_text_color(*self.COR_DESTAQUE)
            self.pdf.cell(8, 5.5, f"{i}.", ln=False)
            self.pdf.set_text_color(*self.COR_TEXTO)
            self.pdf.multi_cell(self._largura_util - 8, 5.5, _texto_pdf(titulo))

            if corpo:
                self.pdf.set_x(self.MARGEM_L + 8)
                self.pdf.set_font("Helvetica", "", 9.5)
                self.pdf.set_text_color(*self.COR_META)
                self.pdf.multi_cell(self._largura_util - 8, 4.8, _texto_pdf(corpo))
            self.pdf.ln(2.2)

    def gerar(self, resultado) -> bytes:
        analise = resultado.analise or {}
        self._nova_pagina()

        from ui.i18n import rotulo_complexidade, rotulo_tipo

        tipo = _texto_pdf(rotulo_tipo(analise.get("tipo_problema", "")) or "N/A")
        nivel = _texto_pdf(rotulo_complexidade(analise.get("complexidade", "")) or "N/A")
        self.pdf.set_font("Helvetica", "B", 10)
        self.pdf.set_text_color(*self.COR_TEXTO)
        self.pdf.cell(0, 6, f"Tema: {tipo}   |   Nivel: {nivel}", ln=True)
        self.pdf.ln(2)

        resumo = _resumo_para_pdf(resultado)
        if resumo:
            self._titulo_secao("Resumo da situacao")
            self._paragrafo(resumo)

        justificativa = limpar_markdown(analise.get("justificativa", ""))
        if justificativa and len(justificativa) > 20 and not contem_erro_tecnico(justificativa):
            self._titulo_secao("Parecer tecnico")
            self._paragrafo(truncar_em_frase(justificativa, 360))

        proximo = extrair_proximo_passo(resultado)
        if proximo:
            self._caixa_destaque("Proxima acao (24-48h)", proximo)

        passos = extrair_passos_detalhados(resultado.plano_acao or "")
        if not passos:
            # Fallback a partir do parecer ("Plano em 3 passos")
            secao_plano = _extrair_secao(
                resultado.relatorio_consolidado or "",
                ("Plano em 3 passos", "Plano de acao", "Plano de ação", "Passo a passo"),
            )
            if secao_plano:
                passos = extrair_passos_detalhados(secao_plano)
        self._passo_a_passo(passos)

        # Conversa resumida
        conversa_fonte = resultado.comunicacao or ""
        bullets = _bullets_de_texto(
            _extrair_secao(
                conversa_fonte,
                (
                    "Abertura da conversa",
                    "Feedback usando SBI",
                    "Perguntas poderosas",
                    "Como conduzir a conversa",
                ),
            )
            or conversa_fonte
        )
        if not bullets:
            bullets = _bullets_de_texto(
                _extrair_secao(
                    resultado.relatorio_consolidado or "",
                    ("Como conduzir a conversa", "Roteiro", "Conversacao", "Conversa"),
                )
            )
        if bullets:
            self._titulo_secao("Como conduzir a conversa (resumo)")
            self._lista_bullets(bullets)

        # Sinais de sucesso
        sinais = _bullets_de_texto(
            _extrair_secao(
                resultado.relatorio_consolidado or "",
                ("Sinais de que esta funcionando", "Sinais de que está funcionando", "Check-in"),
            )
            or _extrair_secao(resultado.plano_acao or "", ("Check-in de acompanhamento", "Riscos e mitigacao", "Riscos e mitigação"))
        )
        if sinais:
            self._titulo_secao("Sinais de que esta funcionando")
            self._lista_bullets(sinais[:4])

        for pagina in range(1, self.pdf.page_no() + 1):
            self.pdf.page = pagina
            self._desenhar_rodape()

        buffer = io.BytesIO()
        self.pdf.output(buffer)
        return buffer.getvalue()


def gerar_pdf_relatorio(resultado) -> bytes:
    return RelatorioPDF().gerar(resultado)
