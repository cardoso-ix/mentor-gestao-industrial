# Imagem base Python 3.11 (leve)
FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    HF_HOME=/home/user/.cache/huggingface \
    TRANSFORMERS_CACHE=/home/user/.cache/huggingface \
    SENTENCE_TRANSFORMERS_HOME=/home/user/.cache/huggingface \
    PORT=7860

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/* \
    && useradd -m -u 1000 user

WORKDIR /app

# PyTorch só CPU — evita ~2 GB de pacotes NVIDIA (mata o cpu-basic do HF)
RUN pip install --no-cache-dir torch --index-url https://download.pytorch.org/whl/cpu

COPY requirements-hf.txt .
RUN pip install --no-cache-dir -r requirements-hf.txt

RUN mkdir -p /home/user/.cache/huggingface && chown -R user:user /home/user

USER user
RUN python -c "from sentence_transformers import SentenceTransformer; SentenceTransformer('paraphrase-multilingual-MiniLM-L12-v2')"

COPY --chown=user:user . .

RUN mkdir -p knowledge_base data/chroma

EXPOSE 7860

CMD ["sh", "-c", "streamlit run main.py --server.address=0.0.0.0 --server.port=${PORT} --server.headless=true --browser.gatherUsageStats=false"]
