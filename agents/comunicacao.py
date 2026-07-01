"""
Agente Especialista em Comunicação.

Monta roteiro prático de conversa com o colaborador,
usando o modelo SBI (Situação, Comportamento, Impacto).
"""

from crewai import Agent, Task

from agents.analista import _criar_llm
from agents.prompts_comuns import REGRAS_QUALIDADE


def criar_agente_comunicacao() -> Agent:
    """Cria o agente Especialista em Comunicação."""
    return Agent(
        role="Especialista em Comunicação para Gestores de Manutenção",
        goal=(
            "Criar um roteiro prático e humanizado para o gestor conduzir "
            "a conversa com o colaborador, usando o modelo SBI e técnicas "
            "de comunicação não violenta."
        ),
        backstory=(
            "Você é coach de comunicação especializado em ambientes industriais. "
            "Sabe que conversas difíceis com técnicos de manutenção exigem "
            "respeito ao conhecimento técnico, objetividade e tom de parceria — "
            "não de cobrança. Domina o modelo SBI (Situação-Comportamento-Impacto) "
            "e adapta a linguagem para o chão de fábrica. Suas frases são curtas, "
            "diretas e fáceis de memorizar antes de uma reunião 1:1."
        ),
        llm=_criar_llm(),
        verbose=False,
        allow_delegation=False,
    )


def criar_task_comunicacao(
    agente: Agent,
    situacao: str,
    analise: dict,
    estrategia: str = "",
    contexto_rag: str = "",
) -> Task:
    """
    Cria a tarefa de comunicação para o agente.

    Args:
        agente: Instância do agente.
        situacao: Situação original.
        analise: Resultado do Analista.
        estrategia: Saída do Estrategista (se já executado).
        contexto_rag: Trechos da base de conhecimento.
    """
    bloco_estrategia = ""
    if estrategia:
        bloco_estrategia = f"\n\n## Estratégia já definida:\n{estrategia}"

    bloco_rag = ""
    if contexto_rag:
        bloco_rag = f"\n\n## Referências:\n{contexto_rag}"

    return Task(
        description=f"""
Crie um roteiro completo para o gestor conduzir a conversa com o colaborador envolvido.

## Situação:
{situacao}

## Análise:
- Tipo: {analise.get('tipo_problema', 'N/A')}
- Resumo: {analise.get('resumo', 'N/A')}
{bloco_estrategia}{bloco_rag}

Estruture sua resposta com estas seções (título em linha própria, terminando com dois pontos):

Preparação antes da conversa:
O que o gestor deve definir antes de chamar o colaborador (2 a 3 pontos concretos).

Abertura da conversa:
2 a 3 frases exatas para iniciar de forma respeitosa e objetiva, usando nomes e fatos do caso.

Feedback usando SBI:
- Situação (S): quando e onde ocorreu, com contexto específico do caso
- Comportamento (B): o que foi observado objetivamente, sem julgamento
- Impacto (I): consequência para equipe, segurança, produção ou processo

Perguntas poderosas:
4 a 5 perguntas abertas para o gestor fazer durante a conversa.

Como lidar com reações:
Sugestões para se o colaborador ficar na defensiva, concordar sem compromisso ou trazer contra-argumentos técnicos.

Fechamento e combinado:
Frases para fechar com acordo claro e próximos passos mensuráveis.

{REGRAS_QUALIDADE}
""",
        expected_output=(
            "Roteiro de comunicação completo com SBI, frases prontas e perguntas"
        ),
        agent=agente,
    )
