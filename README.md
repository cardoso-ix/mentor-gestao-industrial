# Mentor Virtual de Gestão Industrial

Sistema multi-agente que ajuda técnicos e supervisores de **manutenção industrial** a desenvolver habilidades de gestão de pessoas e equipes técnicas.

Quando você descreve uma situação de liderança em linguagem natural, quatro agentes especializados analisam o caso e entregam orientação prática: estratégia de gestão, roteiro de conversa (modelo SBI) e plano de ação com prazos e indicadores.

## Tecnologias

| Componente | Tecnologia |
|------------|------------|
| Orquestração multi-agente | CrewAI |
| LLM | Groq — `llama-3.3-70b-versatile` (gratuito) |
| Busca web | Serper API (processo e segurança) |
| Interface | Streamlit |
| Base de conhecimento | ChromaDB + PDFs locais |
| Embeddings | sentence-transformers (local, gratuito) |
| Deploy | Docker + docker-compose |

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
Gestor/
├── agents/              # Um arquivo por sub-agente
├── knowledge_base/      # Coloque seus PDFs aqui
├── data/chroma/         # Índice persistido (gerado automaticamente)
├── tools/               # Ferramentas (busca web Serper)
├── config.py            # Configurações centralizadas
├── rag.py               # Ingestão e consulta de PDFs
├── orchestrator.py      # Orquestrador principal
├── main.py              # Interface Streamlit
├── requirements.txt
├── .env.example
├── Dockerfile
└── docker-compose.yml
```

## Pré-requisitos

- **Python 3.11 ou 3.12** (desenvolvimento local — o CrewAI ainda não suporta Python 3.14)
- Conta na [Groq](https://console.groq.com) (API key gratuita)
- Conta na [Serper](https://serper.dev) (busca web — plano gratuito disponível)
- Docker e Docker Compose (deploy na VPS — **recomendado também no Windows** se você tiver Python 3.14)

## Configuração

### 1. Clone ou copie o projeto

```bash
cd Gestor
```

### 2. Configure as chaves de API

O arquivo `.env` já foi criado na raiz do projeto. Edite-o e substitua os placeholders:

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

Os PDFs são indexados automaticamente ao iniciar o sistema.

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

## Reindexar PDFs

- **Automático:** ao iniciar o app, PDFs novos ou alterados são indexados
- **Manual:** botão "Reindexar base de conhecimento" na barra lateral

## Limitações e avisos

### Rate limit da Groq (tier gratuito)

Cada análise faz 3–5 chamadas ao LLM. O tier gratuito tem limite de ~30 requisições/minuto. Se atingir o limite, aguarde alguns segundos e tente novamente.

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

## Licença

Projeto de uso educacional e interno. Adapte conforme sua necessidade.
