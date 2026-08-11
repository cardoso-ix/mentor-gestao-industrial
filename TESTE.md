# Checklist para testar a demo

Use este roteiro após o deploy no Hugging Face. Índice completo: [DOCS.md](https://github.com/cardoso-ix/mentor-gestao-industrial/blob/master/DOCS.md).

## Links

| Onde | URL |
|------|-----|
| Demo | https://huggingface.co/spaces/duzinxd/mentor-gestao-industrial |
| Portfólio | https://cardoso-ix.github.io/Portifolio/ |
| Código | https://github.com/cardoso-ix/mentor-gestao-industrial |

## Antes de testar (importante)

1. Confirme no HF → **Settings → Secrets** (ou no `.env` local):
   - `OPENCODE_GO_API_KEY`
   - `SERPER_API_KEY` (opcional se o caso não pedir busca web)
   - `OPENCODE_GO_MODEL=deepseek-v4-flash` (padrão)
   - Opt-in **Enable models hosted in China** no painel OpenCode (Workspace → Go)
2. Se apareceu erro de **cota OpenCode Go**, espere a janela de uso e tente de novo.
3. No Hugging Face, o status do Space deve estar **Running** (não Building/Starting).
4. Se aparecer `RegionError` / China opt-in, ative o toggle no OpenCode e rode de novo.

## Passo a passo do teste

1. Abra a demo (ou rode local: `streamlit run main.py`) e aguarde a tela inicial carregar.
2. (Opcional) Clique em um caso de **Experimente em 1 clique**, ou conte a situação com suas palavras.
3. Ajuste a urgência. Detalhes opcionais só se quiser.
4. Clique em **Gerar orientação** **uma vez** e aguarde (1–3 min).
5. Detalhes de planta ficam em “Detalhes opcionais”, se quiser enriquecer.
6. Verifique:
   - Barra de progresso avança (inclui “Redigindo e validando parecer”)
   - **Parecer executivo** no topo, com tom de mentor sênior e sem frase cortada
   - Abas **Diagnóstico**, **Estratégia**, **Conversa**, **Plano** com conteúdo
   - Sem caixa vermelha de erro
   - PDF com passo a passo completo

## Se der erro de rate limit / cota

- Não clique várias vezes seguidas.
- Aguarde 1–2 minutos e tente de novo.
- O app já faz retry automático; se a cota do OpenCode Go (5h/semana/mês) esgotar, espere a janela liberar.

## Teste local (alternativa)

```bash
cp .env.example .env   # preencha OPENCODE_GO_API_KEY
pip install -r requirements.txt
streamlit run main.py
```

Acesse http://localhost:8501 — usa sua chave do `.env` sem competir com visitantes da demo pública.

**Esperado:** análise completa em cerca de 1–3 minutos, com parecer + abas preenchidas e sem erro vermelho.
