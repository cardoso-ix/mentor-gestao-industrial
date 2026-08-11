"""
Configuração central do projeto.
Carrega variáveis de ambiente do arquivo .env e define valores padrão.
"""

import os
from pathlib import Path

from dotenv import load_dotenv

# Carrega as variáveis do arquivo .env (se existir)
load_dotenv()

# Diretório raiz do projeto
BASE_DIR = Path(__file__).resolve().parent


def _ler_chave(nome: str, padrao: str = "") -> str:
    """Lê variável de ambiente, com fallback para secrets do Streamlit/HF."""
    val = os.getenv(nome, "").strip()
    if val:
        return val
    # Alias genérico usado em alguns deploys
    if nome in {"OPENCODE_GO_API_KEY", "OPENROUTER_API_KEY"}:
        alt = os.getenv("LLM_API_KEY", "").strip()
        if alt:
            return alt
    try:
        import streamlit as st

        if nome in st.secrets:
            return str(st.secrets[nome]).strip()
        # secrets aninhados / tipagem HF às vezes expõem via atributo
        try:
            if hasattr(st.secrets, nome):
                return str(getattr(st.secrets, nome)).strip()
        except Exception:
            pass
        if nome in {"OPENCODE_GO_API_KEY", "OPENROUTER_API_KEY"}:
            for alias in ("LLM_API_KEY", "OPENCODE_GO_API_KEY", "OPENROUTER_API_KEY"):
                if alias in st.secrets and str(st.secrets[alias]).strip():
                    return str(st.secrets[alias]).strip()
    except Exception:
        pass
    return padrao


def refresh_secrets() -> None:
    """Recarrega chaves após o Streamlit disponibilizar os secrets."""
    global OPENCODE_GO_API_KEY, OPENROUTER_API_KEY, SERPER_API_KEY, LLM_API_KEY
    global LLM_PROVIDER, LLM_MODEL, LLM_BASE_URL
    # Re-lê provider (pode vir de secret/env no HF)
    LLM_PROVIDER = os.getenv("LLM_PROVIDER", LLM_PROVIDER or "opencode_go").strip().lower()
    OPENCODE_GO_API_KEY = _ler_chave("OPENCODE_GO_API_KEY")
    OPENROUTER_API_KEY = _ler_chave("OPENROUTER_API_KEY")
    SERPER_API_KEY = _ler_chave("SERPER_API_KEY")
    LLM_API_KEY = _resolver_llm_api_key()
    if LLM_PROVIDER == "opencode_go":
        LLM_MODEL = os.getenv("OPENCODE_GO_MODEL", OPENCODE_GO_MODEL)
        LLM_BASE_URL = os.getenv(
            "OPENCODE_GO_BASE_URL", OPENCODE_GO_BASE_URL
        ).rstrip("/")
    else:
        LLM_MODEL = os.getenv("OPENROUTER_MODEL", OPENROUTER_MODEL)
        LLM_BASE_URL = ""
    # Espelha no ambiente para LiteLLM/CrewAI
    if LLM_API_KEY:
        os.environ["OPENAI_API_KEY"] = LLM_API_KEY
        if LLM_PROVIDER == "opencode_go":
            os.environ["OPENAI_API_BASE"] = LLM_BASE_URL
            os.environ["OPENAI_BASE_URL"] = LLM_BASE_URL
            os.environ["OPENCODE_GO_API_KEY"] = LLM_API_KEY
        else:
            os.environ["OPENROUTER_API_KEY"] = LLM_API_KEY


def _resolver_llm_api_key() -> str:
    """Resolve a chave do provedor LLM ativo (OpenCode Go ou OpenRouter)."""
    if LLM_PROVIDER == "opencode_go":
        return (
            OPENCODE_GO_API_KEY
            or OPENROUTER_API_KEY  # compat: chave antiga/reaproveitada
        )
    return OPENROUTER_API_KEY or OPENCODE_GO_API_KEY


# --- Provedor LLM ---
# Padrão: OpenCode Go + DeepSeek V4 Flash (relatórios dos agentes)
# Alternativa: openrouter (modelos :free)
LLM_PROVIDER = os.getenv("LLM_PROVIDER", "opencode_go").strip().lower()

# --- Chaves de API ---
OPENCODE_GO_API_KEY = _ler_chave("OPENCODE_GO_API_KEY")
OPENROUTER_API_KEY = _ler_chave("OPENROUTER_API_KEY")
SERPER_API_KEY = _ler_chave("SERPER_API_KEY")

# --- OpenCode Go (DeepSeek V4 Flash) ---
OPENCODE_GO_BASE_URL = os.getenv(
    "OPENCODE_GO_BASE_URL", "https://opencode.ai/zen/go/v1"
).rstrip("/")
OPENCODE_GO_MODEL = os.getenv("OPENCODE_GO_MODEL", "deepseek-v4-flash")

# --- OpenRouter (legado / fallback) ---
OPENROUTER_MODEL = os.getenv(
    "OPENROUTER_MODEL", "google/gemma-4-26b-a4b-it:free"
)

# Tokens e ritmo entre agentes
LLM_MAX_TOKENS = int(
    os.getenv(
        "LLM_MAX_TOKENS",
        os.getenv("OPENROUTER_MAX_TOKENS", "2048"),
    )
)
# OpenCode Go tem cota bem maior que o free da OpenRouter — pausa menor por padrão
_PAUSE_PADRAO = "1" if LLM_PROVIDER == "opencode_go" else "3"
LLM_PAUSE_ENTRE_AGENTES = float(
    os.getenv(
        "LLM_PAUSE_ENTRE_AGENTES",
        os.getenv("OPENROUTER_PAUSE_ENTRE_AGENTES", _PAUSE_PADRAO),
    )
)
LLM_RATE_LIMIT_RETRIES = int(
    os.getenv(
        "LLM_RATE_LIMIT_RETRIES",
        os.getenv("OPENROUTER_RATE_LIMIT_RETRIES", "4"),
    )
)
LLM_RATE_LIMIT_ESPERA_BASE = float(
    os.getenv(
        "LLM_RATE_LIMIT_ESPERA_BASE",
        os.getenv("OPENROUTER_RATE_LIMIT_ESPERA_BASE", "10"),
    )
)

# Aliases legados (código antigo / docs)
OPENROUTER_MAX_TOKENS = LLM_MAX_TOKENS
OPENROUTER_PAUSE_ENTRE_AGENTES = LLM_PAUSE_ENTRE_AGENTES
OPENROUTER_RATE_LIMIT_RETRIES = LLM_RATE_LIMIT_RETRIES
OPENROUTER_RATE_LIMIT_ESPERA_BASE = LLM_RATE_LIMIT_ESPERA_BASE

LLM_API_KEY = _resolver_llm_api_key()

if LLM_PROVIDER == "opencode_go":
    LLM_MODEL = OPENCODE_GO_MODEL
    LLM_BASE_URL = OPENCODE_GO_BASE_URL
else:
    LLM_MODEL = OPENROUTER_MODEL
    LLM_BASE_URL = ""

# Placeholders que NÃO devem ser tratados como chave válida
_PLACEHOLDERS_CHAVE = {
    "",
    "sua_chave_openrouter_aqui",
    "sua_chave_opencode_go_aqui",
    "sk-or-sua_chave_real_aqui",
}


def llm_configurado() -> bool:
    """True se há chave válida para o provedor LLM ativo."""
    return bool(LLM_API_KEY) and LLM_API_KEY not in _PLACEHOLDERS_CHAVE


# --- Caminhos de arquivos e pastas ---
KNOWLEDGE_BASE_DIR = Path(os.getenv("KNOWLEDGE_BASE_DIR", BASE_DIR / "knowledge_base"))
CHROMA_PERSIST_DIR = Path(os.getenv("CHROMA_PERSIST_DIR", BASE_DIR / "data" / "chroma"))

# --- Modelo de embeddings local (gratuito, multilíngue) ---
EMBEDDING_MODEL = os.getenv(
    "EMBEDDING_MODEL", "paraphrase-multilingual-MiniLM-L12-v2"
)

# --- Configurações do RAG ---
CHUNK_SIZE = int(os.getenv("CHUNK_SIZE", "500"))
CHUNK_OVERLAP = int(os.getenv("CHUNK_OVERLAP", "50"))
RAG_TOP_K = int(os.getenv("RAG_TOP_K", "5"))

# Nome da coleção no ChromaDB
CHROMA_COLLECTION_NAME = "mentor_gestao_knowledge"

# Arquivo que guarda o hash dos PDFs já indexados (evita reprocessar tudo)
INDEX_MANIFEST_PATH = CHROMA_PERSIST_DIR / "index_manifest.json"
