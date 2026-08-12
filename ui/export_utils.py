"""Exportação PDF — briefing executivo profissional e objetivo."""

from __future__ import annotations

import io
import re
import unicodedata
from datetime import datetime

from ui.text_utils import contem_erro_tecnico, extrair_proximo_passo, limpar_markdown, truncar_em_frase

LIMITE_RESUMO = 340
LIMITE_PROXIMO = 220
LIMITE_PASSO_TITULO = 70
LIMITE_PASSO_ACAO = 130
MAX_PASSOS_PDF = 5
MAX_BULLETS = 4


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
        .replace("\u201c", '"')
        .replace("\u201d", '"')
        .replace("\u2019", "'")
    )


def _truncar(texto: str, limite: int) -> str:
    return truncar_em_frase((texto or "").strip(), limite)


def _limpar_rotulo_passo(texto: str) -> str:
    t = limpar_markdown(texto or "")
    t = re.sub(r"^(Passo\s+\d+\s*[—\-–:]?\s*)", "", t, flags=re.I)
    t = re.sub(r"\s*—\s*-\s*O que fazer:\s*", ": ", t, flags=re.I)
    t = re.sub(r"\s*-\s*O que fazer:\s*", ": ", t, flags=re.I)
    return re.sub(r"\s{2,}", " ", t).strip()


def extrair_passos_detalhados(texto_plano: str) -> list[dict[str, str]]:
    """Extrai passos estruturados do plano de ação."""
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
            saida.append(f"{titulo}: {acao}" if acao else titulo)
        return saida

    passos = []
    for linha in (texto_plano or "").split("\n"):
        linha = linha.strip()
        if re.match(r"^(\*\*)?Passo\s+\d+", linha, re.I) or re.match(r"^\d+[\.\)]\s+", linha):
            passos.append(re.sub(r"^\d+[\.\)]\s+", "", linha))
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


def _bullets_de_texto(texto: str, limite: int = MAX_BULLETS) -> list[str]:
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
            itens.append(_truncar(item, 140))
        if len(itens) >= limite:
            break
    return itens


def _pontos_conversa(resultado) -> list[str]:
    """Puxa poucos pontos de fala, misturando abertura e perguntas."""
    comunicacao = resultado.comunicacao or ""
    consolidado = resultado.relatorio_consolidado or ""
    fontes = [
        _extrair_secao(comunicacao, ("Abertura da conversa", "Abertura")),
        _extrair_secao(comunicacao, ("Perguntas poderosas", "Perguntas")),
        _extrair_secao(comunicacao, ("Feedback usando SBI", "Feedback")),
        _extrair_secao(consolidado, ("Como conduzir a conversa", "Roteiro", "Conversa")),
        comunicacao,
    ]
    vistos: set[str] = set()
    pontos: list[str] = []
    for fonte in fontes:
        for item in _bullets_de_texto(fonte, limite=MAX_BULLETS):
            chave = item.lower()
            if chave in vistos:
                continue
            vistos.add(chave)
            pontos.append(item)
            if len(pontos) >= MAX_BULLETS:
                return pontos
    return pontos


def _resumo_para_pdf(resultado) -> str:
    analise = resultado.analise or {}
    if analise.get("resumo"):
        return _truncar(limpar_markdown(analise["resumo"]), LIMITE_RESUMO)

    parecer = limpar_markdown((resultado.relatorio_consolidado or "").strip())
    secao = _extrair_secao(parecer, ("Parecer executivo", "Resumo", "Diagnostico", "Diagnóstico"))
    if secao and not contem_erro_tecnico(secao):
        return _truncar(secao, LIMITE_RESUMO)
    if parecer and not contem_erro_tecnico(parecer):
        return _truncar(parecer, LIMITE_RESUMO)
    return ""


class RelatorioPDF:
    """Briefing executivo em 1 página (ou 2 se necessário), limpo e apresentável."""

    COR_INK = (28, 25, 23)
    COR_MUTED = (120, 113, 108)
    COR_LINE = (231, 229, 228)
    COR_SURFACE = (250, 250, 249)
    COR_ACCENT = (180, 83, 9)
    COR_ACCENT_SOFT = (255, 247, 237)
    COR_WHITE = (255, 255, 255)
    COR_CHIP_BG = (245, 245, 244)
    COR_HEADER = (28, 25, 23)

    MARGEM = 16
    HEADER_H = 26
    FOOTER_H = 14

    def __init__(self):
        from fpdf import FPDF

        self.data_geracao = datetime.now().strftime("%d/%m/%Y")
        self.pdf = FPDF(orientation="P", unit="mm", format="A4")
        self.pdf.set_auto_page_break(auto=False)
        self.pdf.set_margins(self.MARGEM, self.HEADER_H + 6, self.MARGEM)
        self.largura = self.pdf.w - 2 * self.MARGEM

    def _y_limite(self) -> float:
        return self.pdf.h - self.FOOTER_H - 6

    def _nova_pagina(self):
        self.pdf.add_page()
        self.pdf.set_fill_color(*self.COR_WHITE)
        self.pdf.rect(0, 0, self.pdf.w, self.pdf.h, style="F")
        self._cabecalho()
        self.pdf.set_y(self.HEADER_H + 8)

    def _garantir(self, altura: float):
        if self.pdf.get_y() + altura > self._y_limite():
            self._nova_pagina()

    def _altura_texto(self, texto: str, largura: float, line_h: float, size: float = 9.5) -> float:
        if not texto:
            return 0.0
        self.pdf.set_font("Helvetica", "", size)
        h = self.pdf.multi_cell(
            largura,
            line_h,
            texto,
            dry_run=True,
            output="HEIGHT",
        )
        return float(h)

    def _cabecalho(self):
        self.pdf.set_fill_color(*self.COR_HEADER)
        self.pdf.rect(0, 0, self.pdf.w, self.HEADER_H, style="F")
        self.pdf.set_fill_color(*self.COR_ACCENT)
        self.pdf.rect(0, self.HEADER_H - 1.4, self.pdf.w, 1.4, style="F")

        self.pdf.set_xy(self.MARGEM, 6)
        self.pdf.set_font("Helvetica", "B", 12.5)
        self.pdf.set_text_color(*self.COR_WHITE)
        self.pdf.cell(self.largura * 0.62, 6, _texto_pdf("Mentor de Gestao Industrial"), ln=False)

        self.pdf.set_font("Helvetica", "", 8)
        self.pdf.set_text_color(253, 186, 116)
        self.pdf.cell(
            self.largura * 0.38,
            6,
            _texto_pdf(f"Briefing  ·  {self.data_geracao}"),
            align="R",
            ln=True,
        )

        self.pdf.set_xy(self.MARGEM, 14.5)
        self.pdf.set_font("Helvetica", "", 8)
        self.pdf.set_text_color(214, 211, 209)
        self.pdf.cell(0, 5, _texto_pdf("Orientacao objetiva para supervisores de manutencao"), ln=True)

    def _rodape(self):
        y = self.pdf.h - self.FOOTER_H
        self.pdf.set_draw_color(*self.COR_LINE)
        self.pdf.set_line_width(0.2)
        self.pdf.line(self.MARGEM, y, self.pdf.w - self.MARGEM, y)
        self.pdf.set_xy(self.MARGEM, y + 2.2)
        self.pdf.set_font("Helvetica", "", 7)
        self.pdf.set_text_color(*self.COR_MUTED)
        self.pdf.cell(
            self.largura,
            3.5,
            _texto_pdf(
                f"Eduardo Cardoso  ·  Apoio a supervisao  ·  Pag. {self.pdf.page_no()}"
            ),
            align="C",
            ln=True,
        )
        self.pdf.set_x(self.MARGEM)
        self.pdf.cell(
            self.largura,
            3.2,
            _texto_pdf("Adapte prazos ao contexto da planta. Nao substitui norma interna nem NR."),
            align="C",
        )

    def _secao(self, titulo: str):
        self._garantir(12)
        y = self.pdf.get_y()
        self.pdf.set_fill_color(*self.COR_ACCENT)
        self.pdf.rect(self.MARGEM, y + 1.4, 1.6, 4.6, style="F")
        self.pdf.set_xy(self.MARGEM + 4, y)
        self.pdf.set_font("Helvetica", "B", 9.5)
        self.pdf.set_text_color(*self.COR_INK)
        self.pdf.cell(0, 7, _texto_pdf(titulo.upper()), ln=True)
        self.pdf.ln(0.2)

    def _texto(self, texto: str, size: float = 9.5, cor=None, altura: float = 4.6):
        if not texto:
            return
        self.pdf.set_font("Helvetica", "", size)
        self.pdf.set_text_color(*(cor or self.COR_INK))
        self.pdf.multi_cell(self.largura, altura, _texto_pdf(texto))
        self.pdf.ln(1.2)

    def _chips(self, tipo: str, nivel: str):
        self._garantir(12)
        y = self.pdf.get_y()
        gap = 3.5
        x = self.MARGEM
        for label, valor in (("Tema", tipo), ("Nivel", nivel)):
            valor_t = _texto_pdf(valor or "N/A")
            label_t = _texto_pdf(label)
            self.pdf.set_font("Helvetica", "B", 9)
            w_val = self.pdf.get_string_width(valor_t)
            self.pdf.set_font("Helvetica", "", 7)
            w_lab = self.pdf.get_string_width(label_t)
            chip_w = max(w_val, w_lab) + 10
            chip_w = max(chip_w, 36)

            self.pdf.set_fill_color(*self.COR_CHIP_BG)
            self.pdf.set_draw_color(*self.COR_LINE)
            self.pdf.rect(x, y, chip_w, 9.5, style="DF")
            self.pdf.set_xy(x + 3, y + 1.1)
            self.pdf.set_font("Helvetica", "", 7)
            self.pdf.set_text_color(*self.COR_MUTED)
            self.pdf.cell(chip_w - 6, 3, label_t, ln=True)
            self.pdf.set_x(x + 3)
            self.pdf.set_font("Helvetica", "B", 9)
            self.pdf.set_text_color(*self.COR_INK)
            self.pdf.cell(chip_w - 6, 4.2, valor_t, ln=False)
            x += chip_w + gap
        self.pdf.set_y(y + 12)

    def _caixa_acao(self, titulo: str, conteudo: str):
        if not conteudo:
            return
        texto = _texto_pdf(_truncar(conteudo, LIMITE_PROXIMO))
        texto_h = self._altura_texto(texto, self.largura - 10, 4.6, size=9.5)
        altura = 10 + texto_h
        self._garantir(altura + 3)

        y0 = self.pdf.get_y()
        self.pdf.set_fill_color(*self.COR_ACCENT_SOFT)
        self.pdf.set_draw_color(*self.COR_ACCENT)
        self.pdf.set_line_width(0.45)
        self.pdf.rect(self.MARGEM, y0, self.largura, altura, style="DF")
        self.pdf.set_fill_color(*self.COR_ACCENT)
        self.pdf.rect(self.MARGEM, y0, 1.8, altura, style="F")

        self.pdf.set_xy(self.MARGEM + 5, y0 + 2.2)
        self.pdf.set_font("Helvetica", "B", 7.5)
        self.pdf.set_text_color(*self.COR_ACCENT)
        self.pdf.cell(0, 3.8, _texto_pdf(titulo.upper()), ln=True)
        self.pdf.set_x(self.MARGEM + 5)
        self.pdf.set_font("Helvetica", "", 9.5)
        self.pdf.set_text_color(*self.COR_INK)
        self.pdf.multi_cell(self.largura - 10, 4.6, texto)
        self.pdf.set_y(y0 + altura + 3.2)
        self.pdf.set_line_width(0.2)

    def _passo_card(self, indice: int, titulo: str, acao: str, prazo: str):
        titulo_t = _texto_pdf(_truncar(titulo, LIMITE_PASSO_TITULO))
        acao_t = _texto_pdf(_truncar(acao, LIMITE_PASSO_ACAO)) if acao else ""
        prazo_t = _texto_pdf(_truncar(prazo, 55)) if prazo else ""

        texto_w = self.largura - 14
        acao_h = self._altura_texto(acao_t, texto_w, 4.1, size=8.5) if acao_t else 0
        altura = 8.2 + acao_h + (3.4 if prazo_t else 0)
        altura = max(altura, 11)
        self._garantir(altura + 2.5)

        y0 = self.pdf.get_y()
        self.pdf.set_fill_color(*self.COR_SURFACE)
        self.pdf.set_draw_color(*self.COR_LINE)
        self.pdf.rect(self.MARGEM, y0, self.largura, altura, style="DF")

        self.pdf.set_fill_color(*self.COR_ACCENT)
        self.pdf.ellipse(self.MARGEM + 2.4, y0 + 2.6, 5, 5, style="F")
        self.pdf.set_xy(self.MARGEM + 2.4, y0 + 2.9)
        self.pdf.set_font("Helvetica", "B", 7)
        self.pdf.set_text_color(*self.COR_WHITE)
        self.pdf.cell(5, 4.2, str(indice), align="C", ln=False)

        self.pdf.set_xy(self.MARGEM + 9.5, y0 + 2)
        self.pdf.set_font("Helvetica", "B", 9)
        self.pdf.set_text_color(*self.COR_INK)
        self.pdf.cell(texto_w, 4.4, titulo_t, ln=True)

        if acao_t:
            self.pdf.set_x(self.MARGEM + 9.5)
            self.pdf.set_font("Helvetica", "", 8.5)
            self.pdf.set_text_color(*self.COR_MUTED)
            self.pdf.multi_cell(texto_w, 4.1, acao_t)

        if prazo_t:
            self.pdf.set_x(self.MARGEM + 9.5)
            self.pdf.set_font("Helvetica", "B", 7.5)
            self.pdf.set_text_color(*self.COR_ACCENT)
            self.pdf.cell(0, 3.2, _texto_pdf(f"Prazo: {prazo}"), ln=True)

        self.pdf.set_y(y0 + altura + 2.2)

    def _bullets(self, itens: list[str]):
        for item in itens:
            item_t = _texto_pdf(item)
            h = self._altura_texto(item_t, self.largura - 5, 4.3, size=9)
            self._garantir(h + 2)
            y = self.pdf.get_y()
            self.pdf.set_fill_color(*self.COR_ACCENT)
            self.pdf.ellipse(self.MARGEM + 1, y + 1.5, 1.5, 1.5, style="F")
            self.pdf.set_xy(self.MARGEM + 5, y)
            self.pdf.set_font("Helvetica", "", 9)
            self.pdf.set_text_color(*self.COR_INK)
            self.pdf.multi_cell(self.largura - 5, 4.3, item_t)
            self.pdf.ln(0.8)

    def gerar(self, resultado) -> bytes:
        from ui.i18n import rotulo_complexidade, rotulo_tipo

        analise = resultado.analise or {}
        self._nova_pagina()

        tipo = rotulo_tipo(analise.get("tipo_problema", "")) or "N/A"
        nivel = rotulo_complexidade(analise.get("complexidade", "")) or "N/A"
        self._chips(tipo, nivel)

        resumo = _resumo_para_pdf(resultado)
        if resumo:
            self._secao("Situacao")
            self._texto(resumo)

        proximo = extrair_proximo_passo(resultado)
        if proximo:
            self._caixa_acao("Proxima acao (24h)", proximo)

        passos = extrair_passos_detalhados(resultado.plano_acao or "")
        if not passos:
            secao_plano = _extrair_secao(
                resultado.relatorio_consolidado or "",
                ("Plano em 3 passos", "Plano de acao", "Plano de ação", "Passo a passo"),
            )
            if secao_plano:
                passos = extrair_passos_detalhados(secao_plano)

        if passos:
            self._secao("Plano de acao")
            for i, passo in enumerate(passos[:MAX_PASSOS_PDF], start=1):
                self._passo_card(
                    i,
                    passo.get("titulo") or f"Passo {i}",
                    passo.get("acao") or "",
                    passo.get("prazo") or "",
                )

        bullets = _pontos_conversa(resultado)
        if bullets:
            self._secao("Conversa (pontos-chave)")
            self._bullets(bullets[:MAX_BULLETS])

        # Rodapé em todas as páginas (uma vez cada)
        total = self.pdf.page_no()
        for pagina in range(1, total + 1):
            self.pdf.page = pagina
            self._rodape()

        buffer = io.BytesIO()
        self.pdf.output(buffer)
        return buffer.getvalue()


def gerar_pdf_relatorio(resultado) -> bytes:
    return RelatorioPDF().gerar(resultado)
