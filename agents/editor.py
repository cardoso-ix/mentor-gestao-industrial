"""
Agente Editor de Parecer.

Consolida as saídas dos especialistas em um parecer executivo único,
com tom de mentor sênior de manutenção industrial.
"""

from crewai import Agent, Task

from agents.analista import _criar_llm
from agents.playbooks import montar_bloco_playbook
from agents.prompts_comuns import INSTRUCOES_COMUNS


def criar_agente_editor() -> Agent:
    """Cria o agente Editor de Parecer Executivo."""
    return Agent(
        role="Editor de Parecer Executivo para Gestão Industrial",
        goal=(
            "Transformar análises e recomendações fragmentadas em um parecer "
            "único, claro e acionável para o supervisor no chão de fábrica."
        ),
        backstory=(
            "Você é mentor sênior de gestores de manutenção. Já foi técnico, "
            "supervisor e coordenador de PCM. Escreve pareceres curtos que um "
            "gestor consegue ler entre uma OS e outra, decidir e agir no mesmo dia. "
            "Não repete blocos inteiros dos especialistas: sintetiza, prioriza e "
            "entrega linguagem pronta para uso."
        ),
        llm=_criar_llm(),
        verbose=False,
        allow_delegation=False,
    )


def criar_task_editor(
    agente: Agent,
    situacao: str,
    analise: dict,
    estrategia: str = "",
    comunicacao: str = "",
    plano_acao: str = "",
) -> Task:
    """Cria a tarefa de consolidação do parecer final."""
    bloco_playbook = montar_bloco_playbook(analise.get("tipo_problema", ""))
    if bloco_playbook:
        bloco_playbook = f"\n\n{bloco_playbook}"

    return Task(
        description=f"""
Reescreva as saídas abaixo em UM parecer executivo coerente para o gestor.

## Situação e contexto:
{situacao}

## Análise:
- Tipo: {analise.get('tipo_problema', 'N/A')}
- Complexidade: {analise.get('complexidade', 'N/A')}
- Resumo: {analise.get('resumo', 'N/A')}
- Justificativa: {analise.get('justificativa', 'N/A')}
{bloco_playbook}

## Estratégia (fonte):
{estrategia or 'Não gerada.'}

## Comunicação (fonte):
{comunicacao or 'Não gerada.'}

## Plano de ação (fonte):
{plano_acao or 'Não gerado.'}

Estruture EXATAMENTE nestas seções (título em linha própria, terminando com dois pontos):

Parecer executivo:
2 a 4 frases com o diagnóstico e o que está em jogo operacionalmente.

O que está em jogo:
3 pontos com hífen (equipe, processo/OS/segurança, indicador ou risco).

Ação imediata:
1 ação concreta para as próximas 24 a 48 horas, com responsável implícito (gestor) e critério de sucesso.

Como conduzir a conversa:
Resumo curto com 3 a 5 frases prontas ou bullets no modelo SBI, citando fatos do caso.

Plano em 3 passos:
Três passos priorizados com prazo sugerido em cada um.

Sinais de que está funcionando:
2 a 3 evidências observáveis nos próximos 7 a 14 dias.

Regras adicionais:
- Não copie blocos longos das fontes; sintetize.
- Não invente dados.
- Não use markdown.
- Mantenha o texto legível em menos de 450 palavras.

{INSTRUCOES_COMUNS}
""",
        expected_output=(
            "Parecer executivo consolidado com as seções pedidas, em português brasileiro"
        ),
        agent=agente,
    )
