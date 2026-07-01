# Deploy no Streamlit Cloud — leia antes

Se o app falhou com `pydantic`, `PyO3`, `crewai not found` ou `Python 3.14`, siga **exatamente** estes passos.

## Erros comuns (vistos nos logs)

| Sintoma | Causa |
|---------|--------|
| `Python 3.14.6 environment` | Versão errada — CrewAI exige **&lt; 3.14** |
| `main module: agents/__init__.py` | Arquivo principal errado no painel |
| `No matching distribution found for crewai` | Pip no 3.14 não acha CrewAI ≥ 0.86 |
| `PyO3 maximum supported version (3.13)` | Build de pydantic/tokenizers quebra no 3.14 |

## Configuração correta

1. Acesse [share.streamlit.io](https://share.streamlit.io/)
2. **Apague** o app atual (obrigatório para trocar a versão do Python)
3. **Deploy again** com:

| Campo | Valor |
|-------|--------|
| Repositório | `cardoso-ix/mentor-gestao-industrial` |
| Branch | `master` |
| **Main file path** | `main.py` |
| **Python version** (Advanced settings) | **3.12** |
| Subdomínio | `mentor-gestao-industrial` |

4. Em **Secrets**:

```toml
GROQ_API_KEY = "sua_chave_groq"
SERPER_API_KEY = "sua_chave_serper"
```

5. Clique **Deploy** e aguarde 5–10 min (primeira vez baixa o modelo de embeddings).

## Não use

- `agents/__init__.py` como arquivo principal — isso importa CrewAI na inicialização e quebra o deploy.
- Python 3.14 — incompatível com CrewAI, ChromaDB e sentence-transformers neste projeto.

## Se ainda falhar por memória

O plano gratuito tem ~1 GB RAM. O modelo de embeddings pode estourar ao analisar. Use **Docker na VPS** (ver README).
