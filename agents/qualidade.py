"""Checklist de qualidade do parecer executivo."""

from __future__ import annotations

import re
from dataclasses import dataclass, field

from crewai import Agent, Task

from agents.analista import _criar_llm
from agents.prompts_comuns import INSTRUCOES_COMUNS

_FRASES_GENERICAS = (
    "a comunicação é fundamental",
    "cada caso é único",
    "é importante dialogar",
    "é essencial alinhar",
    "deve-se buscar o diálogo",
    "a liderança deve ser inspiradora",
    "em um mundo ideal",
)

_MARCADORES_PRAZO = (
    "24h",
    "24 h",
    "48h",
    "48 h",
    "hoje",
    "amanhã",
    "amanha",
    "esta semana",
    "dias",
    "prazo",
    "imediata",
)

_MARCADORES_SBI = (
    "situação",
    "situacao",
    "comportamento",
    "impacto",
    "sbi",
    "conversa",
    "feedback",
)


@dataclass
class ResultadoQualidade:
    ok: bool
    falhas: list[str] = field(default_factory=list)
    detalhes: dict[str, bool] = field(default_factory=dict)


def _tokens_uteis(texto: str) -> set[str]:
    stop = {
        "para",
        "como",
        "com",
        "uma",
        "uns",
        "das",
        "dos",
        "que",
        "por",
        "nao",
        "não",
        "mais",
        "menos",
        "este",
        "esta",
        "isso",
        "aqui",
        "sobre",
        "apos",
        "após",
        "quando",
        "onde",
        "muito",
        "pode",
        "deve",
        "fazer",
        "equipe",
        "gestor",
        "tecnico",
        "técnico",
    }
    tokens = set(re.findall(r"[a-zA-ZÀ-ÿ0-9%]{4,}", (texto or "").lower()))
    return {t for t in tokens if t not in stop}


def avaliar_parecer(parecer: str, situacao: str) -> ResultadoQualidade:
    """Avalia o parecer com heurísticas leves (sem chamada extra de LLM)."""
    texto = (parecer or "").strip()
    sit = (situacao or "").strip()
    falhas: list[str] = []
    detalhes: dict[str, bool] = {}

    if len(texto) < 180:
        falhas.append("parecer curto demais para orientar a ação")
        detalhes["tamanho"] = False
    else:
        detalhes["tamanho"] = True

    tokens_sit = _tokens_uteis(sit)
    tokens_par = _tokens_uteis(texto)
    overlap = len(tokens_sit & tokens_par)
    cita_fatos = overlap >= 3 or any(
        trecho.lower() in texto.lower()
        for trecho in re.findall(r"\b[\wÀ-ÿ]{5,}\b", sit)[:12]
        if trecho
    )
    detalhes["cita_fatos"] = bool(cita_fatos)
    if not cita_fatos:
        falhas.append("não citou fatos concretos da situação descrita")

    tem_prazo = any(m in texto.lower() for m in _MARCADORES_PRAZO)
    detalhes["tem_prazo"] = tem_prazo
    if not tem_prazo:
        falhas.append("falta ação com prazo claro (24h, dias, semana)")

    tem_sbi = any(m in texto.lower() for m in _MARCADORES_SBI)
    detalhes["tem_conversa"] = tem_sbi
    if not tem_sbi:
        falhas.append("falta orientação de conversa/SBI utilizável")

    generico = any(f in texto.lower() for f in _FRASES_GENERICAS)
    detalhes["nao_generico"] = not generico
    if generico:
        falhas.append("há frases genéricas de manual")

    secoes = (
        "parecer executivo",
        "ação imediata",
        "acao imediata",
        "plano em 3 passos",
    )
    tem_estrutura = sum(1 for s in secoes if s in texto.lower()) >= 2
    detalhes["estrutura"] = tem_estrutura
    if not tem_estrutura:
        falhas.append("estrutura do parecer está incompleta")

    return ResultadoQualidade(ok=not falhas, falhas=falhas, detalhes=detalhes)


def criar_task_revisao_qualidade(
    agente: Agent,
    situacao: str,
    parecer_atual: str,
    falhas: list[str],
) -> Task:
    """Reescreve apenas o necessário para corrigir falhas de qualidade."""
    lista = "\n".join(f"- {f}" for f in falhas) or "- reforçar especificidade"
    return Task(
        description=f"""
Revise o parecer abaixo corrigindo APENAS estas falhas de qualidade:

{lista}

## Situação original (use fatos daqui):
{situacao}

## Parecer atual:
{parecer_atual}

Entregue o parecer completo revisado, nas mesmas seções:
Parecer executivo:
O que está em jogo:
Ação imediata:
Como conduzir a conversa:
Plano em 3 passos:
Sinais de que está funcionando:

Regras:
- Cite nomes, fatos e tentativas da situação.
- Inclua prazo concreto na ação imediata e nos passos.
- Inclua frases prontas de conversa (SBI) específicas do caso.
- Evite frases genéricas de manual.
- Não invente dados.
- Sem markdown.
- Menos de 450 palavras.

{INSTRUCOES_COMUNS}
""",
        expected_output="Parecer executivo revisado e completo em português brasileiro",
        agent=agente,
    )


def criar_agente_revisor() -> Agent:
    """Revisor curto focado em qualidade operacional."""
    return Agent(
        role="Revisor de Qualidade de Pareceres Industriais",
        goal=(
            "Garantir que o parecer cite fatos do caso, tenha prazo, "
            "conversa utilizável e linguagem específica de manutenção."
        ),
        backstory=(
            "Você revisa pareceres de mentorias para supervisores de manutenção. "
            "Corta genérico, reforça fatos, prazos e frases prontas para a 1:1."
        ),
        llm=_criar_llm(),
        verbose=False,
        allow_delegation=False,
    )
