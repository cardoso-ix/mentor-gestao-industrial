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

# 8501 = Docker local/VPS | Hugging Face Spaces injeta PORT=7860
ENV PORT=8501
EXPOSE 8501

CMD ["sh", "-c", "streamlit run main.py --server.address=0.0.0.0 --server.port=${PORT} --server.headless=true --browser.gatherUsageStats=false"]
