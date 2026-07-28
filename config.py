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
    """Lê variável de ambiente, com fallback para secrets do Streamlit Cloud."""
    val = os.getenv(nome, "").strip()
    if val:
        return val
    try:
        import streamlit as st

        if nome in st.secrets:
            return str(st.secrets[nome]).strip()
    except Exception:
        pass
    return padrao


def refresh_secrets() -> None:
    """Recarrega chaves após o Streamlit disponibilizar os secrets."""
    global OPENROUTER_API_KEY, SERPER_API_KEY
    OPENROUTER_API_KEY = _ler_chave("OPENROUTER_API_KEY")
    SERPER_API_KEY = _ler_chave("SERPER_API_KEY")


# --- Chaves de API ---
OPENROUTER_API_KEY = _ler_chave("OPENROUTER_API_KEY")
SERPER_API_KEY = _ler_chave("SERPER_API_KEY")

# --- Modelo LLM na OpenRouter (variante free — $0/token) ---
# Alternativas: openrouter/free | google/gemma-4-31b-it:free | openai/gpt-oss-20b:free
# Nota: a lista :free muda com frequência; confira em https://openrouter.ai/models
OPENROUTER_MODEL = os.getenv(
    "OPENROUTER_MODEL", "google/gemma-4-26b-a4b-it:free"
)
OPENROUTER_MAX_TOKENS = int(os.getenv("OPENROUTER_MAX_TOKENS", "2048"))

# Pausa entre agentes e retentativas (OpenRouter free: 20 req/min, 50 req/dia sem créditos)
OPENROUTER_PAUSE_ENTRE_AGENTES = float(
    os.getenv("OPENROUTER_PAUSE_ENTRE_AGENTES", "3")
)
OPENROUTER_RATE_LIMIT_RETRIES = int(os.getenv("OPENROUTER_RATE_LIMIT_RETRIES", "4"))
OPENROUTER_RATE_LIMIT_ESPERA_BASE = float(
    os.getenv("OPENROUTER_RATE_LIMIT_ESPERA_BASE", "10")
)

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
