# Imagem base Python 3.11 (leve)
FROM python:3.11-slim

# Evita arquivos .pyc e buffering de stdout
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# Dependências do sistema para sentence-transformers e chromadb
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Instala dependências Python
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Pré-baixa o modelo de embeddings no build (evita timeout no primeiro startup)
RUN python -c "from sentence_transformers import SentenceTransformer; SentenceTransformer('paraphrase-multilingual-MiniLM-L12-v2')"

# Copia o código da aplicação
COPY . .

# Cria pastas necessárias
RUN mkdir -p knowledge_base data/chroma

# Porta padrão do Streamlit
EXPOSE 8501

# Comando de inicialização
CMD ["streamlit", "run", "main.py", "--server.address=0.0.0.0", "--server.port=8501", "--server.headless=true"]
