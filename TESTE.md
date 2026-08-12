# Checklist para testar a demo

Roteiro rápido para validar a demo pública ou o ambiente local.  
Índice: [DOCS.md](DOCS.md)

## Links para testar

| Onde | URL |
|------|-----|
| **Demo (Hugging Face)** | https://huggingface.co/spaces/duzinxd/mentor-gestao-industrial |
| **App direto** | https://duzinxd-mentor-gestao-industrial.hf.space |
| Portfólio | https://cardoso-ix.github.io/Portifolio/ |
| Código | https://github.com/cardoso-ix/mentor-gestao-industrial |

## Antes de testar

1. No Space, status deve estar **Running** (não Building / Starting).
2. Secrets no HF (ou `.env` local):
   - `OPENCODE_GO_API_KEY` (obrigatória)
   - `SERPER_API_KEY` (recomendada)
   - `LLM_PROVIDER=opencode_go` (padrão)
   - `OPENCODE_GO_MODEL=deepseek-v4-flash` (padrão)
3. No OpenCode (Workspace → Go): **Enable models hosted in China** ativado.
4. Remova secrets legados `OPENROUTER_API_KEY` / `GROQ_API_KEY` se ainda existirem.

## Teste em 5 passos (público)

1. Abra a demo e confirme o hero **Mentor de Gestão Industrial** + bloco **Nota geral**.
2. Em **Casos modelo**, clique em um exemplo (ex.: resistência a preencher OS) **ou** escolha o tipo e escreva o caso.
3. Clique em **Gerar briefing** uma vez e aguarde 1–3 min (barra de progresso / “Montando o briefing”).
4. Confira o resultado:
   - Faixa **Orientação pronta** / briefing executivo
   - Prioridade **Faça nas próximas 24 horas**
   - Síntese objetiva
   - Abas **Diagnóstico · Estratégia · Conversa · Plano**
   - Botão **Baixar briefing em PDF**
5. Abra o PDF: 1 página (ou 2), header, chips Tema/Nível, próxima ação, plano e rodapé.

## Casos sugeridos para demo

| Caso modelo | O que observar |
|-------------|----------------|
| Resistência a preencher OS | Desempenho / liderança, plano com prazo |
| Recusa de EPI / LOTO | Segurança + busca Serper (se configurada) |
| Conflito entre turnos | Comunicação / conversa SBI |

## Erros comuns

| Sintoma | O que fazer |
|---------|-------------|
| Space Building / erro ao abrir | Aguarde o build; recarregue em alguns minutos |
| `401 Missing Authentication header` | Confira `OPENCODE_GO_API_KEY` e reinicie o Space |
| `RegionError` / China | Ative **Enable models hosted in China** no OpenCode |
| Limite / cota OpenCode | Aguarde a janela de uso (5h / semana / mês) |
| Limite 10 análises/hora | Aguarde 1h ou teste local |
| Busca web indisponível | Configure `SERPER_API_KEY` (só processo/segurança) |

## Teste local

```bash
cp .env.example .env   # OPENCODE_GO_API_KEY + SERPER_API_KEY
pip install -r requirements.txt
streamlit run main.py
```

Acesse http://localhost:8501

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

**Esperado:** análise completa em ~1–3 min, sem erro vermelho, com parecer + abas + PDF.
