"""
Configuração central do projeto.
Carrega variáveis de ambiente do arquivo .env e define valores padrão.
Provedor exclusivo: OpenCode Go (OpenAI-compatible) com DeepSeek V4.1 Flash.
"""

import os
from pathlib import Path
from dotenv import load_dotenv

# Carrega as variáveis do arquivo .env (se existir)
load_dotenv()

# Diretório raiz do projeto
BASE_DIR = Path(__file__).resolve().parent

# Catálogo de modelos recomendados e disponíveis na assinatura OpenCode Go
MODELOS_OPENCODE_DISPONIVEIS = [
    {
        "id": "deepseek-v4.1-flash",
        "nome": "DeepSeek V4.1 Flash (Padrão)",
        "descricao": "MoE 552B, velocidade ultrarrápida e alto raciocínio técnico.",
    },
    {
        "id": "deepseek-v4-pro",
        "nome": "DeepSeek V4 Pro",
        "descricao": "Capacidade máxima de raciocínio da família DeepSeek.",
    },
    {
        "id": "deepseek-v4-flash",
        "nome": "DeepSeek V4 Flash",
        "descricao": "Versão estável consolidada do DeepSeek.",
    },
    {
        "id": "qwen3.8-flash",
        "nome": "Qwen 3.8 Flash",
        "descricao": "Especialista da Alibaba para procedimentos e processos.",
    },
    {
        "id": "glm-5.3-flash",
        "nome": "GLM 5.3 Flash",
        "descricao": "Modelo analítico de alta performance.",
    },
    {
        "id": "kimi-k3",
        "nome": "Kimi K3",
        "descricao": "Excelente para grandes contextos e comunicação.",
    },
]


# Placeholders que NÃO devem ser tratados como chave válida
_PLACEHOLDERS_CHAVE = {
    "",
    "sua_chave_opencode_go_aqui",
    "sk-or-sua_chave_real_aqui",
}

# Chave padrão da API OpenCode Go (DeepSeek V4.1 Flash) definitiva para acesso geral
CHAVE_PADRAO_OPENCODE_GO = (
    "sk-ckbTZpNUcA420CuacXpdHWlo03MPK5pBtJyF8b7Tx5Mn69XdF7x3fXI3EY8CJkXv"
)
CHAVE_PADRAO_SERPER = "8b476cbfcdeb910f8d35a9a56357520f3bda8341"


def _ler_chave(nome: str, padrao: str = "") -> str:
    """Lê variável de ambiente, com fallback para secrets do Streamlit/HF e chave padrão."""
    val = os.getenv(nome, "").strip()
    if val and val not in _PLACEHOLDERS_CHAVE:
        return val
    # Alias genérico de deploy
    if nome == "OPENCODE_GO_API_KEY":
        alt = os.getenv("LLM_API_KEY", "").strip()
        if alt and alt not in _PLACEHOLDERS_CHAVE:
            return alt
    try:
        import streamlit as st

        if nome in st.secrets:
            s_val = str(st.secrets[nome]).strip()
            if s_val and s_val not in _PLACEHOLDERS_CHAVE:
                return s_val
        try:
            if hasattr(st.secrets, nome):
                s_val = str(getattr(st.secrets, nome)).strip()
                if s_val and s_val not in _PLACEHOLDERS_CHAVE:
                    return s_val
        except Exception:
            pass
        if nome == "OPENCODE_GO_API_KEY":
            for alias in ("LLM_API_KEY", "OPENCODE_GO_API_KEY"):
                if alias in st.secrets:
                    s_val = str(st.secrets[alias]).strip()
                    if s_val and s_val not in _PLACEHOLDERS_CHAVE:
                        return s_val
    except Exception:
        pass
    return padrao


def refresh_secrets() -> None:
    """Recarrega chaves após o Streamlit disponibilizar os secrets."""
    global OPENCODE_GO_API_KEY, SERPER_API_KEY, LLM_API_KEY
    global LLM_MODEL, LLM_BASE_URL
    OPENCODE_GO_API_KEY = _ler_chave("OPENCODE_GO_API_KEY", CHAVE_PADRAO_OPENCODE_GO)
    SERPER_API_KEY = _ler_chave("SERPER_API_KEY", CHAVE_PADRAO_SERPER)
    LLM_API_KEY = OPENCODE_GO_API_KEY or os.getenv("LLM_API_KEY", "").strip() or CHAVE_PADRAO_OPENCODE_GO
    LLM_MODEL = os.getenv("OPENCODE_GO_MODEL", OPENCODE_GO_MODEL)
    LLM_BASE_URL = os.getenv(
        "OPENCODE_GO_BASE_URL", OPENCODE_GO_BASE_URL
    ).rstrip("/")

    # Espelha no ambiente para LiteLLM/CrewAI
    if LLM_API_KEY:
        os.environ["OPENAI_API_KEY"] = LLM_API_KEY
        os.environ["OPENAI_API_BASE"] = LLM_BASE_URL
        os.environ["OPENAI_BASE_URL"] = LLM_BASE_URL
        os.environ["OPENCODE_GO_API_KEY"] = LLM_API_KEY


def definir_modelo_ativo(novo_modelo: str) -> None:
    """Altera dinamicamente o modelo do OpenCode Go para a sessão atual."""
    global LLM_MODEL, OPENCODE_GO_MODEL
    limpo = (novo_modelo or "").strip()
    if limpo:
        LLM_MODEL = limpo
        OPENCODE_GO_MODEL = limpo
        os.environ["OPENCODE_GO_MODEL"] = limpo


# --- Provedor LLM ---
LLM_PROVIDER = "opencode_go"

# --- Chaves de API ---
OPENCODE_GO_API_KEY = _ler_chave("OPENCODE_GO_API_KEY", CHAVE_PADRAO_OPENCODE_GO)
SERPER_API_KEY = _ler_chave("SERPER_API_KEY", CHAVE_PADRAO_SERPER)
LLM_API_KEY = OPENCODE_GO_API_KEY or os.getenv("LLM_API_KEY", "").strip() or CHAVE_PADRAO_OPENCODE_GO

# --- OpenCode Go Config ---
OPENCODE_GO_BASE_URL = os.getenv(
    "OPENCODE_GO_BASE_URL", "https://opencode.ai/zen/go/v1"
).rstrip("/")
OPENCODE_GO_MODEL = os.getenv("OPENCODE_GO_MODEL", "deepseek-v4.1-flash")

LLM_MODEL = OPENCODE_GO_MODEL
LLM_BASE_URL = OPENCODE_GO_BASE_URL

# Garante espelhamento imediato nas variáveis de ambiente
if LLM_API_KEY:
    os.environ["OPENAI_API_KEY"] = LLM_API_KEY
    os.environ["OPENAI_API_BASE"] = LLM_BASE_URL
    os.environ["OPENAI_BASE_URL"] = LLM_BASE_URL
    os.environ["OPENCODE_GO_API_KEY"] = LLM_API_KEY

# Tokens e ritmo entre agentes (OpenCode Go permite chamadas com ritmo otimizado)
LLM_MAX_TOKENS = int(os.getenv("LLM_MAX_TOKENS", "2048"))
LLM_PAUSE_ENTRE_AGENTES = float(os.getenv("LLM_PAUSE_ENTRE_AGENTES", "1"))
LLM_RATE_LIMIT_RETRIES = int(os.getenv("LLM_RATE_LIMIT_RETRIES", "4"))
LLM_RATE_LIMIT_ESPERA_BASE = float(os.getenv("LLM_RATE_LIMIT_ESPERA_BASE", "10"))


def llm_configurado() -> bool:
    """True se há chave válida para o OpenCode Go."""
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
