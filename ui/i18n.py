"""Rótulos e formatação em português brasileiro para a interface."""

from __future__ import annotations

TIPO_PROBLEMA_LABEL = {
    "lideranca": "Liderança",
    "comunicacao": "Comunicação",
    "conflito": "Conflito",
    "desempenho": "Desempenho",
    "processo": "Processo",
    "seguranca": "Segurança",
}

COMPLEXIDADE_LABEL = {
    "baixa": "Baixa",
    "media": "Média",
    "alta": "Alta",
}


def rotulo_tipo(tipo: str) -> str:
    if not tipo:
        return "—"
    chave = tipo.lower().strip()
    return TIPO_PROBLEMA_LABEL.get(chave, tipo.replace("_", " ").title())


def rotulo_complexidade(complexidade: str) -> str:
    if not complexidade:
        return "—"
    chave = complexidade.lower().strip()
    return COMPLEXIDADE_LABEL.get(chave, complexidade.title())
