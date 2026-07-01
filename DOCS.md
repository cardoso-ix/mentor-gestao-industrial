# Documentação do projeto

Índice central da documentação do **Mentor de Gestão Industrial**.

## Links rápidos

| Recurso | URL |
|---------|-----|
| Demo ao vivo | https://huggingface.co/spaces/duzinxd/mentor-gestao-industrial |
| Código-fonte | https://github.com/cardoso-ix/mentor-gestao-industrial |
| Portfólio | https://cardoso-ix.github.io/Portifolio/ |

## Guias

| Documento | Conteúdo |
|-----------|----------|
| [README.md](README.md) | Visão geral, instalação local, arquitetura |
| [DEPLOY.md](DEPLOY.md) | Publicar no Hugging Face, VPS ou Streamlit Cloud |
| [TESTE.md](TESTE.md) | Checklist para validar a demo após deploy |
| [STREAMLIT_CLOUD.md](STREAMLIT_CLOUD.md) | Streamlit Cloud (legado — não recomendado) |
| [PRODUCT.md](PRODUCT.md) | Propósito do produto, usuários, princípios de design |
| [DESIGN.md](DESIGN.md) | Tokens visuais, paleta e tipografia da interface |

## Configuração

| Arquivo | Uso |
|---------|-----|
| [.env.example](.env.example) | Variáveis de ambiente local |
| [.streamlit/secrets.toml.example](.streamlit/secrets.toml.example) | Modelo de secrets (Streamlit Cloud / referência) |
| [config.py](config.py) | Configurações centralizadas no código |

## Stack técnica (versões pinadas)

| Pacote | Versão |
|--------|--------|
| Python | 3.11 (Docker / HF) ou 3.11–3.12 (local) |
| CrewAI | 1.15.1 |
| ChromaDB | ~1.1 |
| Streamlit | 1.x |
| LLM | Groq `llama-3.3-70b-versatile` |

## Sincronização GitHub → Hugging Face

Cada push na branch `master` dispara o workflow [`.github/workflows/sync-to-hub.yml`](.github/workflows/sync-to-hub.yml).

Requisito: secret `HF_TOKEN` no repositório GitHub (permissão write no Hugging Face).

Secrets do app no Space HF: `GROQ_API_KEY`, `SERPER_API_KEY`.
