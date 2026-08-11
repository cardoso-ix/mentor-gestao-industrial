"""
Factory do LLM compatível com a versão atual do CrewAI.

Provedor padrão: OpenCode Go (DeepSeek V4 Flash) via endpoint OpenAI-compatible.
Alternativa: OpenRouter (modelos :free) via prefixo openrouter/.

O CrewAI não aceita mais wrappers LangChain diretamente no parâmetro llm.
Usamos crewai.LLM (LiteLLM por baixo).

Correção: CrewAI marca mensagens com cache_breakpoint (recurso Anthropic).
Vários provedores rejeitam esse campo — MentorLLM remove antes de cada chamada.

Correção OpenCode Go / DeepSeek: thinking mode não aceita tool_choice.
Patchamos litellm.completion para desligar thinking e limpar tools forçados
pelo instructor/structured output do CrewAI.
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

_LITELLM_PATCH_APLICADO = False


def _aplicar_patch_litellm_opencode() -> None:
    """Garante api_base + thinking disabled em todas as chamadas LiteLLM (inclui instructor)."""
    global _LITELLM_PATCH_APLICADO
    if _LITELLM_PATCH_APLICADO or config.LLM_PROVIDER != "opencode_go":
        return
    try:
        import litellm
    except ImportError:
        return

    if getattr(litellm.completion, "_mentor_opencode_patched", False):
        _LITELLM_PATCH_APLICADO = True
        return

    original = litellm.completion

    def completion_patched(*args: Any, **kwargs: Any):
        kwargs = dict(kwargs)
        base = (
            kwargs.get("api_base")
            or kwargs.get("base_url")
            or config.LLM_BASE_URL
            or os.environ.get("OPENAI_API_BASE")
        )
        if base:
            kwargs["api_base"] = base
            kwargs["base_url"] = base
        kwargs["thinking"] = {"type": "disabled"}
        # Structured output via tools/tool_choice quebra o DeepSeek em thinking mode.
        # Neste produto os agentes geram texto/JSON no conteúdo — não usamos tools.
        if kwargs.get("tools") or kwargs.get("tool_choice"):
            kwargs.pop("tools", None)
            kwargs.pop("tool_choice", None)
        return original(*args, **kwargs)

    completion_patched._mentor_opencode_patched = True  # type: ignore[attr-defined]
    litellm.completion = completion_patched
    _LITELLM_PATCH_APLICADO = True


class MentorLLM(LLM):
    """LLM que remove campos incompatíveis injetados pelo CrewAI."""

    @staticmethod
    def _remover_cache_breakpoint(
        messages: str | list[LLMMessage],
    ) -> str | list[LLMMessage]:
        """Remove cache_breakpoint das mensagens (não suportado por vários provedores)."""
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
        """Prepara parâmetros da chamada removendo campos rejeitados pelo provedor."""
        params = super()._prepare_completion_params(
            self._remover_cache_breakpoint(messages),
            tools=tools,
            skip_file_processing=skip_file_processing,
        )
        # LiteLLM usa api_base; CrewAI às vezes só envia base_url — alinhar os dois.
        base = params.get("api_base") or params.get("base_url") or getattr(
            self, "api_base", None
        ) or getattr(self, "base_url", None)
        if base:
            params["api_base"] = base
            params["base_url"] = base

        if config.LLM_PROVIDER == "opencode_go":
            params["thinking"] = {"type": "disabled"}
            params.pop("tools", None)
            params.pop("tool_choice", None)

        return params


# Alias legado
OpenRouterLLM = MentorLLM


def _modelo_opencode_go(modelo: str) -> str:
    """Normaliza o ID do modelo para o provedor OpenAI-compatible do CrewAI/LiteLLM."""
    modelo = (modelo or "").strip()
    if not modelo:
        modelo = "deepseek-v4-flash"
    # Prefixo opencode-go/ é do config do app OpenCode; na API REST o id é limpo
    if modelo.startswith("opencode-go/"):
        modelo = modelo.split("/", 1)[1]
    if not modelo.startswith("openai/"):
        modelo = f"openai/{modelo}"
    return modelo


def _modelo_openrouter(modelo: str) -> str:
    """Normaliza o ID do modelo para o roteamento OpenRouter via LiteLLM."""
    modelo = (modelo or "").strip()
    if not modelo:
        modelo = "google/gemma-4-26b-a4b-it:free"
    if not modelo.startswith("openrouter/"):
        modelo = f"openrouter/{modelo}"
    return modelo


def criar_llm(temperature: float = 0.3) -> MentorLLM:
    """
    Cria instância do LLM para uso nos agentes CrewAI.

    Por padrão usa OpenCode Go + DeepSeek V4 Flash.
    Defina LLM_PROVIDER=openrouter para o caminho legado.

    Args:
        temperature: Criatividade das respostas (0.0 = mais determinístico).

    Returns:
        Instância MentorLLM configurada.
    """
    if not config.llm_configurado():
        raise ValueError(
            "Chave do LLM não configurada. Defina OPENCODE_GO_API_KEY "
            "(ou OPENROUTER_API_KEY) no arquivo .env"
        )

    provedor = config.LLM_PROVIDER
    api_key = config.LLM_API_KEY

    if provedor == "opencode_go":
        # LiteLLM/openai-compatible: chave + base do OpenCode Go (não a API da OpenAI)
        os.environ["OPENAI_API_KEY"] = api_key
        os.environ["OPENAI_API_BASE"] = config.LLM_BASE_URL
        os.environ["OPENAI_BASE_URL"] = config.LLM_BASE_URL
        _aplicar_patch_litellm_opencode()
        return MentorLLM(
            model=_modelo_opencode_go(config.LLM_MODEL),
            api_key=api_key,
            base_url=config.LLM_BASE_URL,
            api_base=config.LLM_BASE_URL,
            temperature=temperature,
            max_tokens=config.LLM_MAX_TOKENS,
            additional_params={"thinking": {"type": "disabled"}},
        )

    # OpenRouter (legado)
    os.environ["OPENROUTER_API_KEY"] = api_key
    return MentorLLM(
        model=_modelo_openrouter(config.LLM_MODEL),
        api_key=api_key,
        temperature=temperature,
        max_tokens=config.LLM_MAX_TOKENS,
    )
