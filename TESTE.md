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
   - `OPENROUTER_API_KEY`
   - `SERPER_API_KEY` (opcional se o caso não pedir busca web)
   - `OPENROUTER_MODEL=google/gemma-4-26b-a4b-it:free` (padrão)
2. Se apareceu erro de **limite OpenRouter** (modelos free: ~50 req/dia), espere e tente no dia seguinte ou use outra chave.
3. No Hugging Face, o status do Space deve estar **Running** (não Building/Starting).

## Passo a passo do teste

1. Abra a demo (ou rode local: `streamlit run main.py`) e aguarde a tela inicial carregar.
2. Conte a situação **com suas palavras** (pode usar o botão de exemplo do tipo).
3. Ajuste a urgência. Detalhes opcionais só se quiser.
4. Clique em **Gerar orientação** **uma vez** e aguarde (1–3 min).
5. Preencha também o **Contexto da planta** (turno, clima, histórico, indicador), se souber — está em “Detalhes opcionais”.
6. Verifique:
   - Barra de progresso avança (inclui “Redigindo e validando parecer”)
   - **Parecer executivo** no topo, com tom de mentor sênior e sem frase cortada
   - Abas **Diagnóstico**, **Estratégia**, **Conversa**, **Plano** com conteúdo
   - Sem caixa vermelha de erro
   - PDF com passo a passo completo

## Se der erro de rate limit

- Não clique várias vezes seguidas.
- Aguarde 1–2 minutos e tente de novo.
- O app já faz retry automático; em pico de uso dos modelos free da OpenRouter pode falhar mesmo assim.

## Teste local (alternativa)

```powershell
cd Gestor
.\venv\Scripts\streamlit.exe run main.py
```

Acesse http://localhost:8501 — usa sua chave do `.env` sem competir com visitantes da demo pública.
