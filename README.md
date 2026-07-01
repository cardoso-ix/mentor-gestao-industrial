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

Sistema multi-agente que ajuda técnicos e supervisores de **manutenção industrial** a desenvolver habilidades de gestão de pessoas e equipes técnicas.

Quando você descreve uma situação de liderança em linguagem natural, quatro agentes especializados analisam o caso e entregam orientação prática: estratégia de gestão, roteiro de conversa (modelo SBI) e plano de ação com prazos e indicadores.

**Demo** · [Hugging Face](https://huggingface.co/spaces/duzinxd/mentor-gestao-industrial) · [Portfólio](https://cardoso-ix.github.io/Portifolio/) · [Documentação](DOCS.md)

## Tecnologias

| Componente | Tecnologia |
|------------|------------|
| Orquestração multi-agente | CrewAI |
| LLM | Groq — `llama-3.3-70b-versatile` (gratuito) |
| Busca web | Serper API (processo e segurança) |
| Interface | Streamlit |
| Base de conhecimento | ChromaDB + PDFs locais |
| Embeddings | sentence-transformers (local, gratuito) |
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
       └── Relatório consolidado
```

## Estrutura do projeto

```
mentor-gestao-industrial/
├── agents/                 # Sub-agentes CrewAI (analista, estrategista, etc.)
├── ui/                     # Componentes Streamlit (wizard, resultado, estilos)
├── knowledge_base/         # PDFs por categoria (gestao, normas, processos)
├── data/chroma/            # Índice ChromaDB (gerado automaticamente)
├── tools/                  # Busca web Serper
├── .github/workflows/      # Sync automático GitHub → Hugging Face
├── config.py               # Configurações centralizadas
├── rag.py                  # Ingestão e consulta RAG
├── orchestrator.py         # Orquestrador multi-agente
├── llm_utils.py            # LLM Groq compatível com CrewAI
├── main.py                 # Interface Streamlit
├── requirements.txt        # Dependências locais / VPS
├── requirements-hf.txt     # Dependências otimizadas para Hugging Face
├── Dockerfile
├── docker-compose.yml
├── DEPLOY.md               # Guia de publicação
├── TESTE.md                # Checklist de validação
└── DOCS.md                 # Índice da documentação
```

## Pré-requisitos

- **Python 3.11 ou 3.12** (desenvolvimento local — o CrewAI ainda não suporta Python 3.14)
- Conta na [Groq](https://console.groq.com) (API key gratuita)
- Conta na [Serper](https://serper.dev) (busca web — plano gratuito disponível)
- Docker e Docker Compose (deploy na VPS — **recomendado também no Windows** se você tiver Python 3.14)

## Configuração

### 1. Clone o repositório

```bash
git clone https://github.com/cardoso-ix/mentor-gestao-industrial.git
cd mentor-gestao-industrial
```

### 2. Configure as chaves de API

Copie o modelo e edite com suas chaves:

```bash
cp .env.example .env
```

```env
GROQ_API_KEY=gsk_sua_chave_real_aqui
SERPER_API_KEY=sua_chave_serper_real_aqui
GROQ_MODEL=llama-3.3-70b-versatile
```

**Onde obter as chaves:**
- Groq: https://console.groq.com → API Keys → Create API Key
- Serper: https://serper.dev → Dashboard → API Key

### 3. Adicione PDFs à base de conhecimento

Coloque arquivos `.pdf` na pasta `knowledge_base/`. Exemplos úteis:

- Manuais de liderança situacional
- Procedimentos internos de manutenção
- Normas de segurança (NR-10, NR-12, etc.)
- Materiais sobre comunicação e feedback

Os PDFs são indexados na **primeira análise** (quando você clica em Analisar situação), não na abertura da página.

## Executar localmente

> **Windows com Python 3.14:** use Docker (seção abaixo) ou instale [Python 3.12](https://www.python.org/downloads/) e crie o venv com `py -3.12 -m venv venv`.

```bash
# Criar ambiente virtual (recomendado)
python -m venv venv
source venv/bin/activate        # Linux/Mac
# ou: venv\Scripts\activate     # Windows

# Instalar dependências
pip install -r requirements.txt

# Iniciar interface
streamlit run main.py
```

Acesse: http://localhost:8501

## Demo pública

**URL:** https://huggingface.co/spaces/duzinxd/mentor-gestao-industrial

| Opção | Quando usar |
|-------|-------------|
| [Hugging Face Spaces](https://huggingface.co/spaces/duzinxd/mentor-gestao-industrial) | Demo pública (ativa) |
| [Docker na VPS](DEPLOY.md#opção-2--vps-com-docker-produção-estável) | Produção estável, mais RAM |
| [Streamlit Cloud](STREAMLIT_CLOUD.md) | Não recomendado |

Deploy e sincronização: ver [DEPLOY.md](DEPLOY.md).

**Checklist de teste:** [TESTE.md](TESTE.md)

## Deploy na VPS (Docker)

```bash
# Na VPS Linux, dentro da pasta do projeto:
docker compose up -d --build

# Ver logs
docker compose logs -f

# Parar
docker compose down
```

Acesse: `http://IP_DA_SUA_VPS:8501`

### Requisitos da VPS

- **Mínimo:** 2 GB RAM
- **Recomendado:** 4 GB RAM (embeddings locais + Streamlit)
- Porta 8501 liberada no firewall

## Como usar

1. Descreva a situação que está enfrentando com sua equipe de manutenção
2. Opcionalmente informe tamanho da equipe e urgência
3. Clique em **Analisar situação**
4. Leia o **Relatório Consolidado** no topo
5. Explore as abas: Análise | Estratégia | Comunicação | Plano de Ação
6. Use **Nova situação** para analisar outro caso

Cada análise é independente — o sistema não mantém histórico de conversas.

## Base de conhecimento (RAG)

- PDFs ficam em `knowledge_base/` (subpastas: `gestao/`, `normas/`, `processos/`).
- A indexação roda na primeira análise ou quando um PDF novo/alterado é detectado.
- O índice persiste em `data/chroma/` entre reinicializações.

## Limitações e avisos

### Rate limit da Groq (tier gratuito)

Cada análise faz **várias chamadas** ao LLM (Analista + agentes especializados). O plano gratuito limita requisições por minuto. O orquestrador faz **pausa entre agentes** e **retry automático**; se ainda falhar, aguarde 1–2 minutos antes de tentar de novo.

### App público

Por padrão o sistema não tem autenticação. Qualquer pessoa com o link pode usar suas APIs. Monitore o uso nas dashboards da Groq e Serper.

### Embeddings locais

A primeira indexação de muitos PDFs pode demorar alguns minutos. Indexações seguintes são rápidas (só processa arquivos novos ou alterados).

### Modelo LLM

O Llama 3.1 70B foi descontinuado na Groq. Este projeto usa o **Llama 3.3 70B Versatile**, substituto oficial com qualidade igual ou superior.

## Exemplo de uso

**Entrada:**
> Um técnico experiente da minha equipe de manutenção elétrica se recusa a preencher a ordem de serviço após concluir intervenções. Diz que é perda de tempo. Outros técnicos começaram a copiar o comportamento.

**Saída esperada:**
- Análise: tipo `desempenho`, complexidade `média`
- Estratégia: liderança situacional para técnico competente mas desmotivado
- Comunicação: roteiro SBI com frases para conversa 1:1
- Plano: passos com prazos e indicador "100% OS preenchidas em 2 semanas"

## Documentação

| Documento | Descrição |
|-----------|-----------|
| [DOCS.md](DOCS.md) | Índice completo |
| [DEPLOY.md](DEPLOY.md) | Publicar no Hugging Face ou VPS |
| [TESTE.md](TESTE.md) | Validar a demo após deploy |
| [PRODUCT.md](PRODUCT.md) | Propósito e princípios do produto |
| [DESIGN.md](DESIGN.md) | Paleta e tipografia |

## Licença

Projeto de uso educacional e interno. Adapte conforme sua necessidade.
