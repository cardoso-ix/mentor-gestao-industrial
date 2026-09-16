"""
Factory do LLM compatível com a versão atual do CrewAI.

Provedor exclusivo: OpenCode Go via endpoint OpenAI-compatible (https://opencode.ai/zen/go/v1).
Modelo padrão: DeepSeek V4.1 Flash (deepseek-v4.1-flash).

Compatibilidade e Correções:
- Remove cache_breakpoint (rejeitado por vários provedores).
- OpenCode Go / DeepSeek: desliga thinking e remove tool_choice incompatível.
- Sempre injeta api_key + api_base + header Bearer (evita 401 Missing Authentication header).
- Permite alternar dinamicamente qualquer modelo do catálogo OpenCode Go.
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
    """Espelha a chave/base no ambiente para LiteLLM e SDKs."""
    if not api_key:
        return
    os.environ["OPENAI_API_KEY"] = api_key
    os.environ["OPENAI_API_BASE"] = config.LLM_BASE_URL
    os.environ["OPENAI_BASE_URL"] = config.LLM_BASE_URL
    os.environ["OPENCODE_GO_API_KEY"] = api_key


def _chave_efetiva(kwargs: dict[str, Any] | None = None) -> str:
    """Resolve a chave OpenCode Go a usar na chamada com fallbacks seguros."""
    kwargs = kwargs or {}
    candidatos = [
        kwargs.get("api_key"),
        config.LLM_API_KEY,
        os.environ.get("OPENCODE_GO_API_KEY"),
        os.environ.get("OPENAI_API_KEY"),
        config.OPENCODE_GO_API_KEY,
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
    if _LITELLM_PATCH_APLICADO:
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
                "Chave do LLM ausente (OPENCODE_GO_API_KEY). "
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

        # Authorization e x-opencode-session explícitos exigidos pelo OpenCode Go
        headers = dict(kwargs.get("extra_headers") or kwargs.get("headers") or {})
        headers["Authorization"] = f"Bearer {api_key}"
        headers["x-opencode-session"] = os.getenv("OPENCODE_SESSION_ID", "mentor-gestao-industrial")
        kwargs["extra_headers"] = headers

        # DeepSeek V4 / V4.1 no OpenCode Go: desativa modo thinking na geração de relatórios
        kwargs["thinking"] = {"type": "disabled"}
        if kwargs.get("tools") or kwargs.get("tool_choice"):
            kwargs.pop("tools", None)
            kwargs.pop("tool_choice", None)
        return original(*args, **kwargs)

    completion_patched._mentor_opencode_patched = True  # type: ignore[attr-defined]
    litellm.completion = completion_patched
    _LITELLM_PATCH_APLICADO = True


class MentorLLM(LLM):
    """LLM customizado para compatibilização total com o OpenCode Go e CrewAI."""

    @staticmethod
    def _remover_cache_breakpoint(
        messages: str | list[LLMMessage],
    ) -> str | list[LLMMessage]:
        """Remove cache_breakpoint das mensagens."""
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
        """Prepara parâmetros da chamada removendo campos rejeitados."""
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

        base = (
            params.get("api_base")
            or params.get("base_url")
            or getattr(self, "api_base", None)
            or getattr(self, "base_url", None)
            or config.LLM_BASE_URL
        )
        if base:
            params["api_base"] = base
            params["base_url"] = base

        params["thinking"] = {"type": "disabled"}
        params.pop("tools", None)
        params.pop("tool_choice", None)
        if api_key:
            headers = dict(params.get("extra_headers") or {})
            headers["Authorization"] = f"Bearer {api_key}"
            headers["x-opencode-session"] = os.getenv("OPENCODE_SESSION_ID", "mentor-gestao-industrial")
            params["extra_headers"] = headers

        return params


def _modelo_opencode_go(modelo: str | None = None) -> str:
    """
    Normaliza o ID do modelo para o provedor OpenAI-compatible do LiteLLM.
    Exemplos:
      'deepseek-v4.1-flash' -> 'openai/deepseek-v4.1-flash'
      'opencode-go/deepseek-chat' -> 'openai/deepseek-chat'
    """
    m = (modelo or config.LLM_MODEL or "deepseek-v4.1-flash").strip()
    if m.startswith("opencode-go/"):
        m = m.split("/", 1)[1]
    if not m.startswith("openai/"):
        m = f"openai/{m}"
    return m


def criar_llm(temperature: float = 0.3, modelo: str | None = None) -> MentorLLM:
    """
    Cria instância do LLM para uso nos agentes CrewAI através do OpenCode Go.

    Args:
        temperature: Criatividade das respostas (0.0 = mais determinístico).
        modelo: ID do modelo específico (opcional; padrão usa config.LLM_MODEL).

    Returns:
        Instância MentorLLM configurada.
    """
    config.refresh_secrets()

    if not config.llm_configurado():
        raise ValueError(
            "Chave do OpenCode Go não configurada. Defina OPENCODE_GO_API_KEY "
            "no arquivo .env ou nos secrets do Hugging Face."
        )

    api_key = config.LLM_API_KEY
    _sincronizar_env_llm(api_key)
    _aplicar_patch_litellm_opencode()

    modelo_final = _modelo_opencode_go(modelo)

    return MentorLLM(
        model=modelo_final,
        api_key=api_key,
        base_url=config.LLM_BASE_URL,
        api_base=config.LLM_BASE_URL,
        temperature=temperature,
        max_tokens=config.LLM_MAX_TOKENS,
        additional_params={"thinking": {"type": "disabled"}},
        extra_headers={
            "Authorization": f"Bearer {api_key}",
            "x-opencode-session": os.getenv("OPENCODE_SESSION_ID", "mentor-gestao-industrial"),
        },
    )
