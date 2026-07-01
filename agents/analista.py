"""
Agente Analista de Situação.

Responsável por ler a descrição do usuário, classificar o tipo de problema,
avaliar a complexidade e definir quais outros agentes devem ser acionados.
"""

from crewai import Agent, Task
from pydantic import BaseModel, Field

from agents.prompts_comuns import REGRAS_QUALIDADE
from llm_utils import criar_llm


class ResultadoAnalise(BaseModel):
    """Estrutura JSON que o Analista deve retornar."""

    tipo_problema: str = Field(
        description="Tipo: lideranca, comunicacao, conflito, desempenho, processo ou seguranca"
    )
    complexidade: str = Field(description="Nível: baixa, media ou alta")
    resumo: str = Field(
        description="Resumo objetivo em 2-3 frases, citando nomes e fatos da situação"
    )
    agentes: list[str] = Field(
        description="Lista de agentes a acionar: estrategista, comunicacao, plano_acao"
    )
    busca_web: bool = Field(
        description="True apenas se tipo for processo ou seguranca e precisar de referências externas"
    )
    justificativa: str = Field(description="Por que essa classificação e roteamento foram escolhidos")


def _criar_llm():
    """Cria a instância do modelo Groq usada por todos os agentes."""
    return criar_llm(temperature=0.3)


def criar_agente_analista() -> Agent:
    """
    Cria o agente Analista de Situação.

    role: Papel do agente no time
    goal: O que ele deve alcançar
    backstory: Contexto que orienta seu comportamento
    """
    return Agent(
        role="Analista de Situação em Gestão Industrial",
        goal=(
            "Analisar a situação descrita pelo gestor de manutenção industrial, "
            "classificar o tipo de problema, avaliar a complexidade e definir "
            "quais especialistas devem ser acionados."
        ),
        backstory=(
            "Você é um consultor sênior com 20 anos de experiência em manutenção "
            "industrial (elétrica, mecânica, instrumentação e PCM). Já foi técnico, "
            "supervisor e gerente de manutenção. Conhece profundamente os desafios "
            "de quem sai do chão de fábrica para liderar equipes técnicas. "
            "Sua função é fazer o diagnóstico inicial antes que os especialistas "
            "entrem em ação."
        ),
        llm=_criar_llm(),
        verbose=False,
        allow_delegation=False,
    )


def criar_task_analista(
    agente: Agent,
    situacao: str,
    tamanho_equipe: str = "",
    urgencia: str = "",
    contexto_rag: str = "",
) -> Task:
    """
    Cria a tarefa de análise para o agente Analista.

    Args:
        agente: Instância do agente Analista.
        situacao: Texto descritivo da situação pelo usuário.
        tamanho_equipe: Informação opcional sobre tamanho da equipe.
        urgencia: Informação opcional sobre urgência.
    """
    contexto_extra = ""
    if tamanho_equipe:
        contexto_extra += f"\nTamanho da equipe: {tamanho_equipe}"
    if urgencia:
        contexto_extra += f"\nUrgência: {urgencia}"

    if urgencia:
        contexto_extra += f"\nUrgência: {urgencia}"

    bloco_rag = ""
    if contexto_rag:
        bloco_rag = f"\n\nReferências internas (use apenas se forem relevantes ao caso):\n{contexto_rag}"

    return Task(
        description=f"""
Analise a seguinte situação relatada por um gestor de manutenção industrial:

---
{situacao}
---
{contexto_extra}{bloco_rag}

{REGRAS_QUALIDADE}

Com base nessa situação, você deve:

1. CLASSIFICAR o tipo de problema em UMA das categorias:
   - lideranca: questões de autoridade, motivação da equipe, transição técnico→gestor
   - comunicacao: falhas de alinhamento, informação, feedback
   - conflito: desentendimentos, resistência, atrito entre pessoas
   - desempenho: baixa produtividade, não cumprimento de tarefas, qualidade
   - processo: falhas em procedimentos, PCM, ordens de serviço, fluxos de trabalho
   - seguranca: riscos, normas NR, EPIs, lockout/tagout, permissão de trabalho

2. AVALIAR a complexidade: baixa, media ou alta

3. RESUMIR a situação em 2-3 frases objetivas

4. DEFINIR quais agentes acionar na lista "agentes":
   - estrategista: abordagens de gestão (exceto casos triviais de complexidade baixa)
   - comunicacao: roteiro de conversa (incluir para comunicacao, conflito, desempenho, lideranca)
   - plano_acao: passos concretos (incluir na maioria dos casos, exceto triviais)

   REGRAS DE ROTEAMENTO:
   - Para comunicacao, conflito, desempenho ou lideranca: incluir comunicacao e plano_acao
   - Para processo ou seguranca: incluir estrategista e plano_acao; comunicacao se houver pessoas envolvidas
   - Estrategista entra em todos exceto complexidade baixa com problema simples
   - busca_web = true APENAS se tipo for processo ou seguranca

5. JUSTIFICAR suas decisões em uma frase

Responda EXCLUSIVAMENTE no formato JSON estruturado solicitado.
""",
        expected_output=(
            "JSON com campos: tipo_problema, complexidade, resumo, agentes, busca_web, justificativa"
        ),
        agent=agente,
        output_json=ResultadoAnalise,
    )
