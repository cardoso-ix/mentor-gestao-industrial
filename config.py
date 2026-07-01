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
    """Lê variável de ambiente e remove espaços extras."""
    return os.getenv(nome, padrao).strip()


# --- Chaves de API ---
GROQ_API_KEY = _ler_chave("GROQ_API_KEY")
SERPER_API_KEY = _ler_chave("SERPER_API_KEY")

# --- Modelo LLM na Groq ---
GROQ_MODEL = os.getenv("GROQ_MODEL", "llama-3.3-70b-versatile")
GROQ_MAX_TOKENS = int(os.getenv("GROQ_MAX_TOKENS", "4096"))

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
