# Publicar a demo online

O **Streamlit Cloud** costuma falhar neste projeto (Python 3.14 no servidor, CrewAI incompatível, limite de memória). Use uma destas opções.

## Opção 1 — Hugging Face Spaces (recomendado, gratuito)

O Docker fixa **Python 3.11** e evita o problema de versão.

### Passo a passo

1. Crie um token em [huggingface.co/settings/tokens](https://huggingface.co/settings/tokens) (permissão **write**).
2. No GitHub, em `cardoso-ix/mentor-gestao-industrial` → **Settings → Secrets and variables → Actions** → **New repository secret**:
   - Nome: `HF_TOKEN`
   - Valor: o token do passo 1
3. Crie o Space em [huggingface.co/new-space](https://huggingface.co/new-space):
   - **Space name:** `mentor-gestao-industrial`
   - **SDK:** **Docker**
   - **Hardware:** CPU basic (grátis)
4. O repositório GitHub já tem o workflow `.github/workflows/sync-to-hub.yml`. Após configurar o `HF_TOKEN`, cada push na branch **`master`** envia o código para o Space.
5. Para sincronizar agora: **Actions** no GitHub → **Sync to Hugging Face Hub** → **Run workflow**.
6. Em **Settings → Variables and secrets** do Space no Hugging Face, adicione os secrets:

   | Nome | Valor |
   |------|--------|
   | `GROQ_API_KEY` | sua chave Groq |
   | `SERPER_API_KEY` | sua chave Serper |

5. Aguarde o build (5–15 min na primeira vez — baixa dependências e o modelo de embeddings).
6. URL pública: `https://huggingface.co/spaces/duzinxd/mentor-gestao-industrial`

### Atualizar o portfólio

Troque o link **Ver demo** em `Portfolio_EDU/index.html` pela URL do Space acima.

---

## Opção 2 — VPS com Docker (produção estável)

Requisitos: Linux, **2–4 GB RAM**, porta 8501 liberada.

```bash
git clone https://github.com/cardoso-ix/mentor-gestao-industrial.git
cd mentor-gestao-industrial
cp .env.example .env   # edite com as chaves
docker compose up -d --build
docker compose logs -f
```

Acesse: `http://IP_DA_VPS:8501`

---

## Opção 3 — Streamlit Cloud (não recomendado)

Só tente se conseguir forçar **Python 3.12** no painel e o app ainda existir na sua conta.

Veja [STREAMLIT_CLOUD.md](STREAMLIT_CLOUD.md). Se aparecer *"You do not have access"* ou Python 3.14 nos logs, abandone e use a Opção 1.

---

## Checklist após publicar

- [ ] Abrir a URL e ver a tela inicial do Mentor
- [ ] Rodar uma análise de teste (confirma Groq + Serper)
- [ ] Atualizar link no portfólio e no LinkedIn
- [ ] Monitorar uso das APIs na Groq e Serper
