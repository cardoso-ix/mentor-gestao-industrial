"""
Factory do LLM compatível com a versão atual do CrewAI.

O CrewAI não aceita mais ChatGroq (LangChain) diretamente no parâmetro llm.
Usamos crewai.LLM com o prefixo groq/ (via LiteLLM).

Correção: CrewAI marca mensagens com cache_breakpoint (recurso Anthropic).
A API Groq rejeita esse campo — GroqLLM remove antes de cada chamada.
"""

from __future__ import annotations

import os
from typing import Any

from crewai import LLM

try:
    from crewai.llms.cache import CACHE_BREAKPOINT_KEY
except ImportError:
    CACHE_BREAKPOINT_KEY = "cache_breakpoint"

try:
    from crewai.utilities.types import LLMMessage
except ImportError:
    LLMMessage = dict  # type: ignore[misc,assignment]

import config


class GroqLLM(LLM):
    """LLM Groq que remove campos incompatíveis injetados pelo CrewAI."""

    @staticmethod
    def _remover_cache_breakpoint(
        messages: str | list[LLMMessage],
    ) -> str | list[LLMMessage]:
        """Remove cache_breakpoint das mensagens (não suportado pela Groq)."""
        if isinstance(messages, str):
            return messages

        limpas: list[LLMMessage] = []
        for msg in messages:
            if isinstance(msg, dict):
                limpas.append(
                    {k: v for k, v in msg.items() if k != CACHE_BREAKPOINT_KEY}  # type: ignore[misc]
                )
            else:
                limpas.append(msg)
        return limpas

    def _prepare_completion_params(
        self,
        messages: str | list[LLMMessage],
        tools: list | None = None,
        skip_file_processing: bool = False,
    ) -> dict[str, Any]:
        """Prepara parâmetros da chamada removendo campos rejeitados pela Groq."""
        return super()._prepare_completion_params(
            self._remover_cache_breakpoint(messages),
            tools=tools,
            skip_file_processing=skip_file_processing,
        )


def criar_llm(temperature: float = 0.3) -> GroqLLM:
    """
    Cria instância do LLM Groq para uso nos agentes CrewAI.

    Args:
        temperature: Criatividade das respostas (0.0 = mais determinístico).

    Returns:
        Instância GroqLLM configurada para Groq.
    """
    if not config.GROQ_API_KEY or config.GROQ_API_KEY == "sua_chave_groq_aqui":
        raise ValueError("GROQ_API_KEY não configurada no arquivo .env")

    # LiteLLM/Groq também lê GROQ_API_KEY do ambiente
    os.environ["GROQ_API_KEY"] = config.GROQ_API_KEY

    modelo = config.GROQ_MODEL
    if not modelo.startswith("groq/"):
        modelo = f"groq/{modelo}"

    return GroqLLM(
        model=modelo,
        api_key=config.GROQ_API_KEY,
        temperature=temperature,
        max_tokens=config.GROQ_MAX_TOKENS,
    )
