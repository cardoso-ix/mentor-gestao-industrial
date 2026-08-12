---
title: Mentor de Gestão Industrial
emoji: 🏭
colorFrom: yellow
colorTo: red
sdk: docker
app_port: 7860
pinned: false
---

# Mentor Virtual de Gestão Industrial

Sistema multi-agente que ajuda **supervisores de manutenção industrial** a conduzir liderança, segurança e desempenho no chão de fábrica.

Você descreve a situação → o mentor entrega um **briefing executivo**: diagnóstico, roteiro de conversa (SBI) e plano de ação com prazos.

## Teste agora (demo pública)

| | |
|---|---|
| **Demo ao vivo** | https://huggingface.co/spaces/duzinxd/mentor-gestao-industrial |
| **App direto** | https://duzinxd-mentor-gestao-industrial.hf.space |
| **Portfólio** | https://cardoso-ix.github.io/Portifolio/ |
| **Código** | https://github.com/cardoso-ix/mentor-gestao-industrial |

### Como testar em 1 minuto

1. Abra a [demo](https://huggingface.co/spaces/duzinxd/mentor-gestao-industrial) e aguarde o status **Running**.
2. Clique em um **caso modelo** (ex.: resistência a preencher OS) **ou** escolha o tipo e descreva o caso.
3. Clique em **Gerar briefing** e aguarde 1–3 minutos.
4. Leia a prioridade das próximas 24h, a síntese e as abas **Diagnóstico · Estratégia · Conversa · Plano**.
5. Baixe o **briefing em PDF**.

Checklist completo: [TESTE.md](TESTE.md) · Índice: [DOCS.md](DOCS.md)

> Limite público: 10 análises/hora. Use fatos concretos (turno, OS, o que já tentou) para uma orientação melhor.

## Tecnologias

| Componente | Tecnologia |
|------------|------------|
| Orquestração multi-agente | CrewAI |
| LLM | OpenCode Go — DeepSeek V4 Flash (`deepseek-v4-flash`) |
| Busca web | Serper API (processo e segurança) |
| Interface | Streamlit |
| Base de conhecimento | ChromaDB + PDFs locais |
| Embeddings | sentence-transformers (local) |
| Deploy | Hugging Face Spaces (Docker) · VPS (docker-compose) |

## Arquitetura dos agentes

```
Usuário (Streamlit)
       │
       ▼
Orquestrador (orchestrator.py)
       │
       ├── RAG (consulta PDFs em knowledge_base/)
       │
       ├── 1. Analista de Situação (sempre)
       │      → classifica problema, complexidade, roteamento
       │
       ├── Serper (se processo ou segurança)
       │
       ├── 2. Estrategista de Gestão (conforme necessidade)
       ├── 3. Especialista em Comunicação (conforme necessidade)
       ├── 4. Gerador de Plano de Ação (conforme necessidade)
       │
       └── 5. Editor de Parecer Executivo (consolidação final)
```

## Estrutura do projeto

```
mentor-gestao-industrial/
├── agents/                 # Sub-agentes CrewAI
├── ui/                     # Streamlit (wizard, resultado, PDF, estilos)
├── knowledge_base/         # PDFs (gestao, normas, processos)
├── data/chroma/            # Índice ChromaDB
├── tools/                  # Busca web Serper
├── .github/workflows/      # Sync GitHub → Hugging Face
├── config.py
├── rag.py
├── orchestrator.py
├── llm_utils.py
├── main.py                 # Interface Streamlit
├── requirements.txt
├── requirements-hf.txt
├── Dockerfile
├── docker-compose.yml
├── DEPLOY.md
├── TESTE.md
└── DOCS.md
```

## Pré-requisitos (local)

- **Python 3.11 ou 3.12**
- Conta [OpenCode Go](https://opencode.ai) (API key)
- Conta [Serper](https://serper.dev) (plano gratuito disponível)
- Docker (opcional; recomendado no Windows com Python 3.14)

## Configuração local

```bash
git clone https://github.com/cardoso-ix/mentor-gestao-industrial.git
cd mentor-gestao-industrial
cp .env.example .env
```

```env
LLM_PROVIDER=opencode_go
OPENCODE_GO_API_KEY=sua_chave_opencode_go_aqui
OPENCODE_GO_MODEL=deepseek-v4-flash
SERPER_API_KEY=sua_chave_serper_aqui
```

**Chaves:** [opencode.ai](https://opencode.ai) → Workspace → Go / API Keys · [serper.dev](https://serper.dev) → API Key  

**Opt-in China (obrigatório para DeepSeek V4 Flash):** no painel OpenCode, ative **Enable models hosted in China**.

> Alternativa legada: `LLM_PROVIDER=openrouter` + `OPENROUTER_API_KEY`.

## Executar localmente

```bash
python -m venv venv
source venv/bin/activate        # Linux/Mac
# ou: venv\Scripts\activate     # Windows
pip install -r requirements.txt
streamlit run main.py
```

Acesse: http://localhost:8501

## Demo pública e deploy

| Opção | Quando usar |
|-------|-------------|
| [Hugging Face Spaces](https://huggingface.co/spaces/duzinxd/mentor-gestao-industrial) | Demo pública (ativa) |
| [Docker na VPS](DEPLOY.md#opção-2--vps-com-docker) | Produção estável |
| [Streamlit Cloud](STREAMLIT_CLOUD.md) | Não recomendado |

Push em `master` dispara o sync automático para o Space. Detalhes: [DEPLOY.md](DEPLOY.md).

## Como usar

1. (Opcional) Carregue um **caso modelo**, ou selecione o **tipo da situação**.
2. Descreva o caso com fatos (nomes, OS, turno, o que já tentou).
3. Ajuste urgência/equipe e clique em **Gerar briefing** (1–3 min).
4. Leia a ação das próximas 24h e a síntese.
5. Explore as abas e baixe o **briefing em PDF**.

Cada análise é independente — sem histórico de conversas.

## Limitações

- **Cota OpenCode Go:** várias chamadas LLM por análise; o orquestrador faz pausa e retry.
- **App público:** sem autenticação; monitore uso no OpenCode e na Serper.
- **Embeddings:** primeira indexação de PDFs pode demorar; as seguintes são rápidas.

## Exemplo

**Entrada:**  
> Técnico sênior da elétrica se recusa a preencher OS. Outros começaram a copiar.

**Saída esperada:**  
tipo `desempenho` · prioridade 24h · roteiro SBI · plano com prazos · PDF.

## Documentação

| Documento | Descrição |
|-----------|-----------|
| [DOCS.md](DOCS.md) | Índice |
| [TESTE.md](TESTE.md) | Checklist da demo |
| [DEPLOY.md](DEPLOY.md) | Publicar no HF / VPS |
| [PRODUCT.md](PRODUCT.md) | Propósito e princípios |
| [DESIGN.md](DESIGN.md) | Visual |

## Licença

Uso educacional e interno. Adapte conforme sua necessidade.
