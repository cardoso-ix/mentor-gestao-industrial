"""
Factory do LLM compatível com a versão atual do CrewAI.

Provedor padrão: OpenCode Go (DeepSeek V4 Flash) via endpoint OpenAI-compatible.
Alternativa: OpenRouter (modelos :free) via prefixo openrouter/.

O CrewAI não aceita mais wrappers LangChain diretamente no parâmetro llm.
Usamos crewai.LLM (LiteLLM por baixo).

Correções:
- Remove cache_breakpoint (rejeitado por vários provedores).
- OpenCode Go / DeepSeek: desliga thinking e remove tool_choice incompatível.
- Sempre injeta api_key + api_base (evita 401 Missing Authentication header).
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


def _sincronizar_env_llm(api_key: str) -> None:
    """Espelha a chave/base no ambiente para LiteLLM, instructor e SDKs."""
    if not api_key:
        return
    os.environ["OPENAI_API_KEY"] = api_key
    if config.LLM_PROVIDER == "opencode_go":
        os.environ["OPENAI_API_BASE"] = config.LLM_BASE_URL
        os.environ["OPENAI_BASE_URL"] = config.LLM_BASE_URL
        os.environ["OPENCODE_GO_API_KEY"] = api_key
    else:
        os.environ["OPENROUTER_API_KEY"] = api_key


def _chave_efetiva(kwargs: dict[str, Any] | None = None) -> str:
    """Resolve a chave a usar na chamada, com vários fallbacks."""
    kwargs = kwargs or {}
    candidatos = [
        kwargs.get("api_key"),
        config.LLM_API_KEY,
        os.environ.get("OPENAI_API_KEY"),
        os.environ.get("OPENCODE_GO_API_KEY"),
        os.environ.get("OPENROUTER_API_KEY"),
        config.OPENCODE_GO_API_KEY,
        config.OPENROUTER_API_KEY,
    ]
    for valor in candidatos:
        if not valor:
            continue
        texto = str(valor).strip()
        if texto and texto not in config._PLACEHOLDERS_CHAVE:
            return texto
    return ""


def _aplicar_patch_litellm_opencode() -> None:
    """Garante api_key + api_base + thinking disabled em todas as chamadas LiteLLM."""
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
        api_key = _chave_efetiva(kwargs)
        if not api_key:
            raise ValueError(
                "Chave do LLM ausente na chamada (OPENCODE_GO_API_KEY). "
                "Configure no .env ou nos secrets do Hugging Face."
            )
        kwargs["api_key"] = api_key
        _sincronizar_env_llm(api_key)

        base = (
            kwargs.get("api_base")
            or kwargs.get("base_url")
            or config.LLM_BASE_URL
            or os.environ.get("OPENAI_API_BASE")
        )
        if base:
            kwargs["api_base"] = base
            kwargs["base_url"] = base

        # Authorization explícito — evita 401 Missing Authentication header
        headers = dict(kwargs.get("extra_headers") or kwargs.get("headers") or {})
        headers["Authorization"] = f"Bearer {api_key}"
        kwargs["extra_headers"] = headers

        kwargs["thinking"] = {"type": "disabled"}
        # Structured output via tools/tool_choice quebra o DeepSeek em thinking mode.
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
        api_key = _chave_efetiva(params) or getattr(self, "api_key", None) or ""
        api_key = str(api_key).strip()
        if api_key:
            params["api_key"] = api_key
            _sincronizar_env_llm(api_key)

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
            if api_key:
                headers = dict(params.get("extra_headers") or {})
                headers["Authorization"] = f"Bearer {api_key}"
                params["extra_headers"] = headers

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
    # Streamlit/HF podem liberar secrets depois do import inicial
    config.refresh_secrets()

    if not config.llm_configurado():
        raise ValueError(
            "Chave do LLM não configurada. Defina OPENCODE_GO_API_KEY "
            "(ou OPENROUTER_API_KEY) no arquivo .env / secrets do Hugging Face."
        )

    provedor = config.LLM_PROVIDER
    api_key = config.LLM_API_KEY
    _sincronizar_env_llm(api_key)

    if provedor == "opencode_go":
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
    return MentorLLM(
        model=_modelo_openrouter(config.LLM_MODEL),
        api_key=api_key,
        temperature=temperature,
        max_tokens=config.LLM_MAX_TOKENS,
    )
