"""
Agente Gerador de Plano de Ação.

Cria plano objetivo com passos concretos, prazos sugeridos
e indicadores simples para acompanhamento.
"""

from crewai import Agent, Task

from agents.analista import _criar_llm
from agents.prompts_comuns import REGRAS_QUALIDADE


def criar_agente_plano_acao() -> Agent:
    """Cria o agente Gerador de Plano de Ação."""
    return Agent(
        role="Gerador de Plano de Ação para Gestores de Manutenção",
        goal=(
            "Transformar a análise e estratégia em um plano de ação concreto, "
            "com passos claros, prazos realistas e indicadores simples de acompanhamento."
        ),
        backstory=(
            "Você é especialista em execução e acompanhamento de planos de melhoria "
            "em manutenção industrial. Sabe que gestores de chão de fábrica não têm "
            "tempo para planos complexos — precisam de ações objetivas que caibam "
            "entre uma parada programada e outra. Seus planos são realistas para "
            "equipes de 5 a 30 técnicos, com prazos de 24 horas a 30 dias."
        ),
        llm=_criar_llm(),
        verbose=False,
        allow_delegation=False,
    )


def criar_task_plano_acao(
    agente: Agent,
    situacao: str,
    analise: dict,
    estrategia: str = "",
    comunicacao: str = "",
    contexto_rag: str = "",
) -> Task:
    """
    Cria a tarefa de plano de ação para o agente.

    Args:
        agente: Instância do agente.
        situacao: Situação original.
        analise: Resultado do Analista.
        estrategia: Saída do Estrategista (se disponível).
        comunicacao: Saída do agente de Comunicação (se disponível).
        contexto_rag: Trechos da base de conhecimento.
    """
    bloco_estrategia = f"\n\n## Estratégia:\n{estrategia}" if estrategia else ""
    bloco_comunicacao = f"\n\n## Roteiro de comunicação:\n{comunicacao}" if comunicacao else ""
    bloco_rag = f"\n\n## Referências:\n{contexto_rag}" if contexto_rag else ""

    return Task(
        description=f"""
Crie um plano de ação prático para o gestor resolver a situação descrita.

## Situação:
{situacao}

## Análise:
- Tipo: {analise.get('tipo_problema', 'N/A')}
- Complexidade: {analise.get('complexidade', 'N/A')}
- Resumo: {analise.get('resumo', 'N/A')}
{bloco_estrategia}{bloco_comunicacao}{bloco_rag}

Estruture o plano assim (título em linha própria, terminando com dois pontos):

Plano de ação:
Para cada passo (entre 3 e 7), use o formato:

Passo N — Título curto
- O que fazer: descrição clara e objetiva ligada ao caso
- Prazo sugerido: ex. 24h, 3 dias, 1 semana
- Responsável: gestor, colaborador ou equipe
- Indicador de sucesso: como saber que deu certo

Cronograma resumido:
Lista passo × prazo.

Riscos e mitigação:
2 a 3 riscos e o que fazer se acontecer.

Check-in de acompanhamento:
Quando e como o gestor deve revisar o progresso.

{REGRAS_QUALIDADE}
""",
        expected_output=(
            "Plano de ação com passos numerados, prazos, responsáveis e indicadores"
        ),
        agent=agente,
    )
