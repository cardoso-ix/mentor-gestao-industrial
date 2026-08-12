# Deploy da demo online

A demo oficial está no **Hugging Face Spaces** e está aberta para teste público.

| Link | URL |
|------|-----|
| **Demo** | https://huggingface.co/spaces/duzinxd/mentor-gestao-industrial |
| **App direto** | https://duzinxd-mentor-gestao-industrial.hf.space |
| Portfólio | https://cardoso-ix.github.io/Portifolio/ |
| Checklist | [TESTE.md](TESTE.md) |

---

## Opção 1 — Hugging Face Spaces (recomendado)

Docker com Python 3.11, sincronizado automaticamente com o GitHub.

### Pré-requisitos (uma vez)

1. Conta em [huggingface.co](https://huggingface.co) (usuário `duzinxd` ou o seu).
2. Token **write** em [huggingface.co/settings/tokens](https://huggingface.co/settings/tokens).
3. Secret `HF_TOKEN` em [GitHub → Settings → Secrets → Actions](https://github.com/cardoso-ix/mentor-gestao-industrial/settings/secrets/actions).
4. Space criado com **SDK Docker**, nome `mentor-gestao-industrial`, template **Blank**.

### Secrets no Space (obrigatório)

Em **Settings → Secrets** do Space:

| Nome | Valor |
|------|--------|
| `OPENCODE_GO_API_KEY` | Chave do [OpenCode Go](https://opencode.ai) |
| `SERPER_API_KEY` | Chave da [Serper](https://serper.dev) |
| `OPENCODE_GO_MODEL` | `deepseek-v4-flash` (opcional; já é o padrão) |
| `LLM_PROVIDER` | `opencode_go` (opcional; já é o padrão) |

No painel OpenCode, ative **Enable models hosted in China** para o DeepSeek V4 Flash.

Remova secrets antigos (`OPENROUTER_API_KEY`, `GROQ_API_KEY`) para evitar confusão.

### Publicar alterações

```bash
git push origin master
```

O workflow **Sync to Hugging Face Hub** envia o código ao Space. Build leva alguns minutos.

Sincronização manual: [Actions → Run workflow](https://github.com/cardoso-ix/mentor-gestao-industrial/actions/workflows/sync-to-hub.yml).

Depois do sync: no Space, use **Factory reboot** se a análise ainda falhar com secrets antigos em cache.

### Portfólio

O card **Mentor de Gestão Industrial** em [cardoso-ix.github.io/Portifolio](https://cardoso-ix.github.io/Portifolio/) aponta para a demo.  
Texto/stack do card: aplique [docs/PORTFOLIO-SYNC.md](docs/PORTFOLIO-SYNC.md) no repo `Portifolio` (este agente não tem push lá).

---

## Opção 2 — VPS com Docker

Para produção com mais RAM e controle total.

**Requisitos:** Linux, 2–4 GB RAM, porta 8501 liberada.

```bash
git clone https://github.com/cardoso-ix/mentor-gestao-industrial.git
cd mentor-gestao-industrial
cp .env.example .env   # edite OPENCODE_GO_API_KEY e SERPER_API_KEY
docker compose up -d --build
docker compose logs -f
```

Acesse: `http://IP_DA_VPS:8501`

---

## Opção 3 — Streamlit Cloud (legado)

Não recomendado (Python 3.14 no servidor, CrewAI incompatível, limite de memória).

Consulte [STREAMLIT_CLOUD.md](STREAMLIT_CLOUD.md) apenas se precisar tentar.

---

## Checklist pós-deploy

- [x] Demo no Hugging Face publicada
- [x] Sync GitHub → HF ativo
- [ ] Secrets OpenCode Go + Serper no Space
- [ ] Opt-in **Enable models hosted in China** no OpenCode
- [ ] Análise de teste ok — ver [TESTE.md](TESTE.md)
- [ ] Card do portfólio com stack OpenCode Go / DeepSeek (ver [PORTFOLIO-SYNC.md](docs/PORTFOLIO-SYNC.md))
- [ ] Description do repositório GitHub alinhada (sem citar Groq)
- [ ] Uso das APIs monitorado em [opencode.ai](https://opencode.ai) e [serper.dev](https://serper.dev)
