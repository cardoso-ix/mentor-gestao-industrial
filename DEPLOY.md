# Deploy da demo online

A demo oficial está no **Hugging Face Spaces**. O Streamlit Cloud não é recomendado para este projeto.

**Demo ativa:** https://huggingface.co/spaces/duzinxd/mentor-gestao-industrial

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
| `GROQ_API_KEY` | Chave da [Groq](https://console.groq.com) |
| `SERPER_API_KEY` | Chave da [Serper](https://serper.dev) |

### Publicar alterações

```bash
git push origin master
```

O workflow **Sync to Hugging Face Hub** envia o código ao Space. Build leva 5–15 min na primeira vez.

Sincronização manual: [Actions → Run workflow](https://github.com/cardoso-ix/mentor-gestao-industrial/actions/workflows/sync-to-hub.yml).

### Portfólio

O link **Ver demo** em [cardoso-ix.github.io/Portifolio](https://cardoso-ix.github.io/Portifolio/) já aponta para o Space.

---

## Opção 2 — VPS com Docker

Para produção com mais RAM e controle total.

**Requisitos:** Linux, 2–4 GB RAM, porta 8501 liberada.

```bash
git clone https://github.com/cardoso-ix/mentor-gestao-industrial.git
cd mentor-gestao-industrial
cp .env.example .env   # edite com as chaves
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
- [x] Link no portfólio atualizado
- [ ] Secrets Groq e Serper configurados no Space
- [ ] Análise de teste concluída — ver [TESTE.md](TESTE.md)
- [ ] Uso das APIs monitorado em [console.groq.com](https://console.groq.com) e [serper.dev](https://serper.dev)
