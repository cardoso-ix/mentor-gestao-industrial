# Checklist para testar a demo

Use este roteiro após o deploy no Hugging Face. Índice completo: [DOCS.md](https://github.com/cardoso-ix/mentor-gestao-industrial/blob/master/DOCS.md).

## Links

| Onde | URL |
|------|-----|
| Demo | https://huggingface.co/spaces/duzinxd/mentor-gestao-industrial |
| Portfólio | https://cardoso-ix.github.io/Portifolio/ |
| Código | https://github.com/cardoso-ix/mentor-gestao-industrial |

## Antes de testar (importante)

1. Confirme no HF → **Settings → Secrets**:
   - `GROQ_API_KEY`
   - `SERPER_API_KEY`
2. Se apareceu erro de **limite Groq**, espere **pelo menos 1 hora** sem novas análises.
3. No Hugging Face, o status do Space deve estar **Running** (não Building/Starting).

## Passo a passo do teste

1. Abra a demo e aguarde a tela inicial carregar.
2. Cole uma situação curta, por exemplo:

   > Um técnico experiente se recusa a preencher a ordem de serviço após as intervenções. Outros técnicos começaram a copiar o comportamento.

3. Clique em **Analisar situação** **uma vez** e aguarde (1–3 min).
4. Verifique:
   - Barra de progresso avança
   - Abas **Análise**, **Estratégia**, **Comunicação**, **Plano de Ação** com conteúdo
   - Sem caixa vermelha de erro

## Se der erro de rate limit

- Não clique várias vezes seguidas.
- Aguarde 1–2 minutos e tente de novo.
- O app já faz retry automático; em pico de uso da Groq pode falhar mesmo assim.

## Teste local (alternativa)

```powershell
cd Gestor
.\venv\Scripts\streamlit.exe run main.py
```

Acesse http://localhost:8501 — usa sua chave do `.env` sem competir com visitantes da demo pública.
