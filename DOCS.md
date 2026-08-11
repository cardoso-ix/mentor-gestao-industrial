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
| [llm_utils.py](llm_utils.py) | Factory do LLM (OpenCode Go / OpenRouter) |

## Stack técnica

| Pacote | Versão / nota |
|--------|----------------|
| Python | 3.11 (Docker / HF) ou 3.11–3.12 (local) |
| CrewAI | 1.15.1 |
| LiteLLM | ≥ 1.60 (via CrewAI) |
| ChromaDB | ~1.1 |
| Streamlit | 1.x |
| LLM | OpenCode Go — DeepSeek V4 Flash (`deepseek-v4-flash`) |
| Busca web | Serper API |

## Secrets (Hugging Face Space)

| Secret | Obrigatório | Notas |
|--------|-------------|--------|
| `OPENCODE_GO_API_KEY` | Sim | Chave do plano Go em https://opencode.ai |
| `SERPER_API_KEY` | Recomendado | Busca web em casos de processo/segurança |
| `LLM_PROVIDER` | Não | Padrão: `opencode_go` |
| `OPENCODE_GO_MODEL` | Não | Padrão: `deepseek-v4-flash` |
| `OPENCODE_GO_BASE_URL` | Não | Padrão: `https://opencode.ai/zen/go/v1` |

No painel OpenCode (Workspace → Go), ative **Enable models hosted in China** para o DeepSeek V4 Flash.

> Não use mais `OPENROUTER_API_KEY` / `GROQ_API_KEY` como provedor principal.

## Sincronização GitHub → Hugging Face

Cada push na branch `master` dispara o workflow [`.github/workflows/sync-to-hub.yml`](.github/workflows/sync-to-hub.yml).

Requisito: secret `HF_TOKEN` no repositório GitHub (permissão write no Hugging Face).

## LLM e geração de relatórios

Fluxo: RAG → Analista → (Serper se processo/segurança) → Estrategista / Comunicação / Plano → Editor de parecer.

Endpoint: `https://opencode.ai/zen/go/v1` · Modelo: `deepseek-v4-flash`.

Caminho legado: `LLM_PROVIDER=openrouter` + `OPENROUTER_API_KEY`.

## Troubleshooting rápido

| Erro | Ação |
|------|------|
| `401 Missing Authentication header` | Conferir `OPENCODE_GO_API_KEY` e reiniciar o Space |
| `RegionError` | Opt-in China no painel OpenCode |
| Resposta vazia intermitente | Tentar de novo; o orquestrador já faz retry |
| Busca web indisponível | Configurar `SERPER_API_KEY` |
