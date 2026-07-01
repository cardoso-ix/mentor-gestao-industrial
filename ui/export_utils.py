"""Utilitários de exportação PDF resumido."""

from __future__ import annotations

import io
import re
import unicodedata
from datetime import datetime

from ui.text_utils import contem_erro_tecnico, extrair_proximo_passo, limpar_markdown

LIMITE_RESUMO = 320
LIMITE_PROXIMO_PASSO = 220
LIMITE_PASSO = 140
MAX_PASSOS_PDF = 3


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


def extrair_passos_plano(texto_plano: str) -> list[str]:
    if not texto_plano:
        return []

    passos = []
    for linha in texto_plano.split("\n"):
        linha = linha.strip()
        if re.match(r"^(\*\*)?Passo\s+\d+", linha, re.I) or re.match(r"^\d+[\.\)]\s+", linha):
            passos.append(re.sub(r"^\d+[\.\)]\s+", "", linha))
        elif linha.startswith("- O que fazer:") and passos:
            passos[-1] += f" — {linha}"

    if not passos:
        blocos = re.split(r"\n(?=\*\*Passo|\d+[\.\)])", texto_plano)
        passos = [limpar_markdown(b)[:200] for b in blocos if b.strip()][:7]

    if not passos and texto_plano.strip():
        passos = [limpar_markdown(texto_plano)[:300]]

    return [p for p in passos if p and not contem_erro_tecnico(p)][:10]


def _resumo_para_pdf(resultado) -> str:
    analise = resultado.analise or {}
    if analise.get("resumo"):
        return _truncar(limpar_markdown(analise["resumo"]), LIMITE_RESUMO)

    relatorio = limpar_markdown((resultado.relatorio_consolidado or "").strip())
    if relatorio and not contem_erro_tecnico(relatorio):
        return _truncar(relatorio, LIMITE_RESUMO)
    return ""


class RelatorioPDF:
    COR_FUNDO = (255, 255, 255)
    COR_FUNDO_DESTAQUE = (255, 247, 237)
    COR_TEXTO = (15, 45, 74)
    COR_TEXTO_SECUNDARIO = (100, 116, 139)
    COR_DESTAQUE = (230, 126, 34)
    COR_BORDA = (226, 232, 240)
    COR_HEADER = (15, 45, 74)
    COR_HEADER_TEXTO = (255, 255, 255)

    MARGEM_L = 15
    MARGEM_R = 15
    ALTURA_HEADER = 24
    ALTURA_FOOTER = 14

    def __init__(self):
        from fpdf import FPDF

        self.data_geracao = datetime.now().strftime("%d/%m/%Y %H:%M")
        self.pdf = FPDF(orientation="P", unit="mm", format="A4")
        self.pdf.set_auto_page_break(auto=True, margin=self.ALTURA_FOOTER + 4)
        self.pdf.set_margins(self.MARGEM_L, self.ALTURA_HEADER + 4, self.MARGEM_R)
        self._largura_util = self.pdf.w - self.MARGEM_L - self.MARGEM_R

    def _pintar_fundo(self):
        self.pdf.set_fill_color(*self.COR_FUNDO)
        self.pdf.rect(0, 0, self.pdf.w, self.pdf.h, style="F")

    def _desenhar_cabecalho(self):
        self.pdf.set_fill_color(*self.COR_HEADER)
        self.pdf.rect(0, 0, self.pdf.w, self.ALTURA_HEADER, style="F")
        self.pdf.set_fill_color(*self.COR_DESTAQUE)
        self.pdf.rect(0, self.ALTURA_HEADER - 1.2, self.pdf.w, 1.2, style="F")

        self.pdf.set_xy(self.MARGEM_L, 6)
        self.pdf.set_font("Helvetica", "B", 13)
        self.pdf.set_text_color(*self.COR_HEADER_TEXTO)
        self.pdf.cell(0, 6, _texto_pdf("MENTOR DE GESTAO INDUSTRIAL"), ln=False)

        self.pdf.set_font("Helvetica", "", 8)
        self.pdf.set_text_color(200, 220, 235)
        self.pdf.set_xy(self.MARGEM_L, 14)
        self.pdf.cell(self._largura_util, 4, _texto_pdf(self.data_geracao), align="R")
        self.pdf.set_y(self.ALTURA_HEADER + 5)

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
            _texto_pdf(f"(c) Eduardo Cardoso - Todos os direitos reservados  |  Pag. {self.pdf.page_no()}"),
            align="C",
        )

    def _nova_pagina(self):
        self.pdf.add_page()
        self._pintar_fundo()
        self._desenhar_cabecalho()

    def _titulo_secao(self, titulo: str):
        if self.pdf.get_y() > self.pdf.h - 35:
            self._nova_pagina()
        y = self.pdf.get_y()
        self.pdf.set_fill_color(*self.COR_DESTAQUE)
        self.pdf.rect(self.MARGEM_L, y, 2.5, 7, style="F")
        self.pdf.set_xy(self.MARGEM_L + 5, y)
        self.pdf.set_font("Helvetica", "B", 11)
        self.pdf.set_text_color(*self.COR_TEXTO)
        self.pdf.cell(0, 7, _texto_pdf(titulo), ln=True)
        self.pdf.ln(1)

    def _paragrafo(self, texto: str):
        if not texto:
            return
        if self.pdf.get_y() > self.pdf.h - self.ALTURA_FOOTER - 12:
            self._nova_pagina()
        self.pdf.set_font("Helvetica", "", 10)
        self.pdf.set_text_color(*self.COR_TEXTO)
        self.pdf.multi_cell(self._largura_util, 5.2, _texto_pdf(texto))
        self.pdf.ln(2)

    def _caixa_destaque(self, titulo: str, conteudo: str):
        if not conteudo:
            return
        texto = _texto_pdf(_truncar(conteudo, LIMITE_PROXIMO_PASSO))
        y0 = self.pdf.get_y()
        altura = 16 + max(1, len(texto) // 75) * 5
        if y0 + altura > self.pdf.h - self.ALTURA_FOOTER - 5:
            self._nova_pagina()
            y0 = self.pdf.get_y()

        self.pdf.set_fill_color(*self.COR_FUNDO_DESTAQUE)
        self.pdf.set_draw_color(*self.COR_DESTAQUE)
        self.pdf.rect(self.MARGEM_L, y0, self._largura_util, altura, style="DF")
        self.pdf.set_xy(self.MARGEM_L + 4, y0 + 3)
        self.pdf.set_font("Helvetica", "B", 9)
        self.pdf.set_text_color(*self.COR_DESTAQUE)
        self.pdf.cell(0, 4, _texto_pdf(titulo), ln=True)
        self.pdf.set_x(self.MARGEM_L + 4)
        self.pdf.set_font("Helvetica", "", 10)
        self.pdf.set_text_color(*self.COR_TEXTO)
        self.pdf.multi_cell(self._largura_util - 8, 5, texto)
        self.pdf.set_y(y0 + altura + 3)

    def _lista_passos(self, passos: list[str]):
        if not passos:
            return
        self._titulo_secao("Acoes prioritarias (24 h)")
        for i, passo in enumerate(passos[:MAX_PASSOS_PDF], start=1):
            texto = _truncar(limpar_markdown(passo), LIMITE_PASSO)
            if self.pdf.get_y() > self.pdf.h - self.ALTURA_FOOTER - 10:
                self._nova_pagina()
            self.pdf.set_font("Helvetica", "B", 10)
            self.pdf.set_text_color(*self.COR_DESTAQUE)
            self.pdf.cell(8, 5, f"{i}.", ln=False)
            self.pdf.set_font("Helvetica", "", 10)
            self.pdf.set_text_color(*self.COR_TEXTO)
            self.pdf.multi_cell(self._largura_util - 8, 5.2, _texto_pdf(texto))
            self.pdf.ln(1)

    def gerar(self, resultado) -> bytes:
        analise = resultado.analise or {}
        self._nova_pagina()

        from ui.i18n import rotulo_complexidade, rotulo_tipo

        tipo = _texto_pdf(rotulo_tipo(analise.get("tipo_problema", "")) or "N/A")
        nivel = _texto_pdf(rotulo_complexidade(analise.get("complexidade", "")) or "N/A")
        self.pdf.set_font("Helvetica", "B", 10)
        self.pdf.set_text_color(*self.COR_TEXTO)
        self.pdf.cell(0, 6, f"Tema: {tipo}  |  Nivel: {nivel}", ln=True)
        self.pdf.ln(2)

        resumo = _resumo_para_pdf(resultado)
        if resumo:
            self._titulo_secao("Resumo da situacao")
            self._paragrafo(resumo)

        proximo = extrair_proximo_passo(resultado)
        if proximo:
            self._caixa_destaque("Proxima acao", proximo)

        passos = extrair_passos_plano(resultado.plano_acao or "")
        self._lista_passos(passos)

        for pagina in range(1, self.pdf.page_no() + 1):
            self.pdf.page = pagina
            self._desenhar_rodape()

        buffer = io.BytesIO()
        self.pdf.output(buffer)
        return buffer.getvalue()


def gerar_pdf_relatorio(resultado) -> bytes:
    return RelatorioPDF().gerar(resultado)
