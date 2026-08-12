# Documentação do projeto

Índice do **Mentor de Gestão Industrial**.

## Testar agora

| Recurso | URL |
|---------|-----|
| **Demo ao vivo** | https://huggingface.co/spaces/duzinxd/mentor-gestao-industrial |
| **App direto** | https://duzinxd-mentor-gestao-industrial.hf.space |
| Código-fonte | https://github.com/cardoso-ix/mentor-gestao-industrial |
| Portfólio | https://cardoso-ix.github.io/Portifolio/ |
| Checklist de teste | [TESTE.md](TESTE.md) |

Fluxo rápido: caso modelo → **Gerar briefing** → prioridade 24h + abas + PDF.

## Guias

| Documento | Conteúdo |
|-----------|----------|
| [README.md](README.md) | Visão geral, demo, instalação |
| [TESTE.md](TESTE.md) | Como validar a demo pública |
| [DEPLOY.md](DEPLOY.md) | Publicar no Hugging Face / VPS |
| [STREAMLIT_CLOUD.md](STREAMLIT_CLOUD.md) | Streamlit Cloud (legado) |
| [PRODUCT.md](PRODUCT.md) | Propósito, usuários, princípios |
| [DESIGN.md](DESIGN.md) | Tokens visuais da interface |
| [PORTFOLIO-SYNC.md](docs/PORTFOLIO-SYNC.md) | Texto/links do card no portfólio (aplicar no repo Portifolio) |

## Configuração

| Arquivo | Uso |
|---------|-----|
| [.env.example](.env.example) | Variáveis locais |
| [.streamlit/secrets.toml.example](.streamlit/secrets.toml.example) | Modelo de secrets |
| [config.py](config.py) | Config central |
| [llm_utils.py](llm_utils.py) | LLM OpenCode Go / OpenRouter |

## Stack

| Pacote | Versão / nota |
|--------|----------------|
| Python | 3.11 (Docker / HF) ou 3.11–3.12 (local) |
| CrewAI | 1.15.x |
| Streamlit | 1.x |
| ChromaDB | ~1.1 |
| LLM | OpenCode Go — DeepSeek V4 Flash (`deepseek-v4-flash`) |
| Busca web | Serper API |

## Secrets (Hugging Face Space)

| Secret | Obrigatório | Notas |
|--------|-------------|--------|
| `OPENCODE_GO_API_KEY` | Sim | https://opencode.ai |
| `SERPER_API_KEY` | Recomendado | Processo / segurança |
| `LLM_PROVIDER` | Não | Padrão: `opencode_go` |
| `OPENCODE_GO_MODEL` | Não | Padrão: `deepseek-v4-flash` |
| `OPENCODE_GO_BASE_URL` | Não | Padrão: `https://opencode.ai/zen/go/v1` |

No OpenCode (Workspace → Go), ative **Enable models hosted in China**.

## Sync GitHub → Hugging Face

Push em `master` → workflow [`.github/workflows/sync-to-hub.yml`](.github/workflows/sync-to-hub.yml).  
Requisito: secret `HF_TOKEN` no GitHub.

## Troubleshooting

| Erro | Ação |
|------|------|
| `401 Missing Authentication header` | Conferir `OPENCODE_GO_API_KEY` e reiniciar o Space |
| `RegionError` | Opt-in China no OpenCode |
| Resposta vazia | Tentar de novo (há retry) |
| Busca web indisponível | Configurar `SERPER_API_KEY` |
| Limite 10/hora | Aguarde ou rode local |
