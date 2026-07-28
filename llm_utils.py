"""
Factory do LLM compatível com a versão atual do CrewAI.

O CrewAI não aceita mais wrappers LangChain diretamente no parâmetro llm.
Usamos crewai.LLM com o prefixo openrouter/ (via LiteLLM).

Correção: CrewAI marca mensagens com cache_breakpoint (recurso Anthropic).
Vários provedores da OpenRouter rejeitam esse campo — OpenRouterLLM remove
antes de cada chamada.
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


class OpenRouterLLM(LLM):
    """LLM OpenRouter que remove campos incompatíveis injetados pelo CrewAI."""

    @staticmethod
    def _remover_cache_breakpoint(
        messages: str | list[LLMMessage],
    ) -> str | list[LLMMessage]:
        """Remove cache_breakpoint das mensagens (não suportado pela maioria dos free models)."""
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
        """Prepara parâmetros da chamada removendo campos rejeitados pela OpenRouter."""
        return super()._prepare_completion_params(
            self._remover_cache_breakpoint(messages),
            tools=tools,
            skip_file_processing=skip_file_processing,
        )


def criar_llm(temperature: float = 0.3) -> OpenRouterLLM:
    """
    Cria instância do LLM OpenRouter (modelo free) para uso nos agentes CrewAI.

    Args:
        temperature: Criatividade das respostas (0.0 = mais determinístico).

    Returns:
        Instância OpenRouterLLM configurada para OpenRouter.
    """
    if (
        not config.OPENROUTER_API_KEY
        or config.OPENROUTER_API_KEY == "sua_chave_openrouter_aqui"
    ):
        raise ValueError("OPENROUTER_API_KEY não configurada no arquivo .env")

    # LiteLLM lê OPENROUTER_API_KEY do ambiente
    os.environ["OPENROUTER_API_KEY"] = config.OPENROUTER_API_KEY

    modelo = config.OPENROUTER_MODEL
    if not modelo.startswith("openrouter/"):
        modelo = f"openrouter/{modelo}"

    return OpenRouterLLM(
        model=modelo,
        api_key=config.OPENROUTER_API_KEY,
        temperature=temperature,
        max_tokens=config.OPENROUTER_MAX_TOKENS,
    )
