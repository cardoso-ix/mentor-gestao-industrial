"""
Agente Estrategista de Gestão.

Sugere abordagens práticas baseadas em frameworks de gestão,
adaptadas ao contexto de equipes técnicas de manutenção industrial.
"""

from crewai import Agent, Task

from agents.analista import _criar_llm
from agents.prompts_comuns import INSTRUCOES_COMUNS


def criar_agente_estrategista() -> Agent:
    """Cria o agente Estrategista de Gestão."""
    return Agent(
        role="Estrategista de Gestão para Manutenção Industrial",
        goal=(
            "Propor abordagens práticas e fundamentadas para resolver a situação, "
            "usando frameworks de gestão adaptados ao contexto de equipes técnicas "
            "de manutenção industrial."
        ),
        backstory=(
            "Você é mentor de gestão em plantas industriais. Domina liderança "
            "situacional, gestão por competências e comunicação direta no chão de "
            "fábrica. Já liderou equipes de elétrica, mecânica, caldeiraria e PCM. "
            "Técnicos valorizam clareza e respeito ao conhecimento técnico — não "
            "discurso motivacional. Suas recomendações cabem na rotina entre OS, "
            "parada e reunião de turno."
        ),
        llm=_criar_llm(),
        verbose=False,
        allow_delegation=False,
    )


def criar_task_estrategista(
    agente: Agent,
    situacao: str,
    analise: dict,
    contexto_rag: str = "",
    contexto_web: str = "",
) -> Task:
    """
    Cria a tarefa de estratégia para o agente Estrategista.

    Args:
        agente: Instância do agente.
        situacao: Situação original do usuário.
        analise: Resultado da análise do Analista (dict).
        contexto_rag: Trechos relevantes da base de conhecimento.
        contexto_web: Resultados da busca web (se houver).
    """
    bloco_rag = ""
    if contexto_rag:
        bloco_rag = f"\n\n## Referências da base de conhecimento:\n{contexto_rag}"

    bloco_web = ""
    if contexto_web:
        bloco_web = f"\n\n## Informações da busca web:\n{contexto_web}"

    return Task(
        description=f"""
Com base na situação e na análise já realizada, elabore uma estratégia de gestão prática.

## Situação original:
{situacao}

## Análise do Analista:
- Tipo: {analise.get('tipo_problema', 'N/A')}
- Complexidade: {analise.get('complexidade', 'N/A')}
- Resumo: {analise.get('resumo', 'N/A')}
{bloco_rag}{bloco_web}

Elabore sua resposta com estas seções (título em linha própria, terminando com dois pontos):

Diagnóstico estratégico:
Explique a raiz provável do problema no contexto de manutenção industrial, citando fatos da situação.

Abordagem recomendada:
Indique qual framework aplicar (liderança situacional, CNV ou gestão por competências) e por que se encaixa neste caso.

Passos estratégicos:
Liste 3 a 5 ações em ordem de prioridade, específicas para o caso.

Armadilhas a evitar:
Aponte 2 a 3 erros comuns que gestores de manutenção cometem neste tipo de situação.

{INSTRUCOES_COMUNS}
""",
        expected_output=(
            "Estratégia de gestão estruturada com diagnóstico, abordagem, passos e armadilhas"
        ),
        agent=agente,
    )
