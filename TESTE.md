# Checklist para testar a demo

Use este roteiro após o deploy no Hugging Face ou ao validar localmente.
Índice completo: [DOCS.md](DOCS.md).

## Links

| Onde | URL |
|------|-----|
| Demo | https://huggingface.co/spaces/duzinxd/mentor-gestao-industrial |
| Portfólio | https://cardoso-ix.github.io/Portifolio/ |
| Código | https://github.com/cardoso-ix/mentor-gestao-industrial |

## Antes de testar (importante)

1. Confirme no HF → **Settings → Secrets** (ou no `.env` local):
   - `OPENCODE_GO_API_KEY` (obrigatória)
   - `SERPER_API_KEY` (recomendada; usada em processo/segurança)
   - `LLM_PROVIDER=opencode_go` (padrão)
   - `OPENCODE_GO_MODEL=deepseek-v4-flash` (padrão)
2. No painel OpenCode (Workspace → Go), ative **Enable models hosted in China**.
3. No Hugging Face, o status do Space deve estar **Running** (não Building/Starting).
4. Remova secrets antigos `OPENROUTER_API_KEY` / `GROQ_API_KEY` se ainda existirem.

## Passo a passo do teste

1. Abra a demo (ou rode local: `streamlit run main.py`) e aguarde a tela inicial carregar.
2. (Opcional) Clique em um caso de **Experimente em 1 clique**, ou conte a situação com suas palavras.
3. Ajuste a urgência. Detalhes opcionais só se quiser.
4. Clique em **Gerar orientação** **uma vez** e aguarde (1–3 min).
5. Verifique:
   - Barra de progresso avança (inclui “Redigindo e validando parecer”)
   - **Parecer executivo** no topo, com tom de mentor sênior e sem frase cortada
   - Abas **Diagnóstico**, **Estratégia**, **Conversa**, **Plano** com conteúdo
   - Sem caixa vermelha de erro
   - PDF com passo a passo completo

## Erros comuns

| Sintoma | O que fazer |
|---------|-------------|
| `401 Missing Authentication header` | Confira `OPENCODE_GO_API_KEY` nos secrets/`.env` e reinicie o Space |
| `RegionError` / China opt-in | Ative **Enable models hosted in China** no OpenCode |
| Limite / cota OpenCode Go | Aguarde a janela de uso (5h / semana / mês) |
| Busca web indisponível | Configure `SERPER_API_KEY` (só afeta processo/segurança) |

## Teste local

```bash
cp .env.example .env   # preencha OPENCODE_GO_API_KEY e SERPER_API_KEY
pip install -r requirements.txt
streamlit run main.py
```

Acesse http://localhost:8501

**Esperado:** análise completa em cerca de 1–3 minutos, com parecer + abas preenchidas e sem erro vermelho.

### Validação automática (opcional)

```bash
python - <<'PY'
from dotenv import load_dotenv
load_dotenv('.env', override=True)
from orchestrator import executar_mentoria
r = executar_mentoria(
    situacao='Técnico sênior se recusa a preencher OS e outros copiaram.',
    tamanho_equipe='6-10 técnicos',
    urgencia='Média — resolver esta semana',
    categoria_rag='gestao',
)
print('OK' if not r.erro and r.relatorio_consolidado else r.erro)
PY
```
