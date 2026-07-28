"""
Playbooks de mentoria por tipo de problema.

Templates estáveis (sem custo de API) que guiam estratégia, conversa e plano.
"""

from __future__ import annotations

PLAYBOOKS_MENTORIA: dict[str, dict[str, str]] = {
    "lideranca": {
        "nome": "Liderança no chão de fábrica",
        "foco": (
            "Recuperar autoridade com respeito técnico, sem humilhar e sem omitir o padrão."
        ),
        "diagnostico": (
            "Verifique se o problema é autoridade, exemplo ruim do referência técnica "
            "ou falta de consequência clara. Separe competência técnica de comportamento."
        ),
        "conversa": (
            "Use SBI com fatos públicos do turno. Reconheça a competência técnica, "
            "nomeie o comportamento e combine um padrão observável. Evite discussão "
            "de ego na frente da equipe."
        ),
        "plano": (
            "1) Conversa 1:1 em 24h. 2) Alinhamento curto com a equipe em até 3 dias. "
            "3) Acompanhamento de 7 dias com critério visível (ex.: adesão ao combinado)."
        ),
        "armadilhas": (
            "Cobrar na frente da equipe; ameaçar sem critério; elogiar só a técnica e "
            "ignorar o impacto comportamental."
        ),
    },
    "comunicacao": {
        "nome": "Comunicação e alinhamento de turno",
        "foco": (
            "Restaurar fluxo de informação útil entre pessoas/turnos, com ritual simples."
        ),
        "diagnostico": (
            "Identifique onde a informação quebra (passagem de turno, OS, rádio, quadro) "
            "e qual impacto operacional isso gera."
        ),
        "conversa": (
            "Abra com o impacto operacional, não com acusação. Peça o que a pessoa "
            "precisa para informar melhor e feche com um ritual mínimo (o quê, quando, para quem)."
        ),
        "plano": (
            "1) Definir ritual de passagem em 24-48h. 2) Testar por 1 semana. "
            "3) Revisar falhas de informação no check-in semanal."
        ),
        "armadilhas": (
            "Criar formulário complexo; pedir 'mais comunicação' sem formato; "
            "culpar só um turno sem olhar o processo."
        ),
    },
    "conflito": {
        "nome": "Conflito entre pessoas ou turnos",
        "foco": (
            "Desarmar atrito com fatos, papéis claros e acordo operacional."
        ),
        "diagnostico": (
            "Separe conflito interpessoal de falha de processo. Liste fatos recentes "
            "(datas, equipamentos, OS) e o custo do atrito."
        ),
        "conversa": (
            "Fale com cada lado primeiro (fatos e impacto). Depois conduza um alinhamento "
            "conjunto com regras de passagem/entrega. Sem plateia."
        ),
        "plano": (
            "1) Escuta individual em 24-48h. 2) Acordo conjunto em até 3 dias. "
            "3) Acompanhar 7-14 dias com indicador simples (atraso, retrabalho, ocorrência)."
        ),
        "armadilhas": (
            "Mediar no corredor; forçar pedido de desculpas vazio; mudar dupla sem tratar a causa."
        ),
    },
    "desempenho": {
        "nome": "Desempenho e padrão de trabalho",
        "foco": (
            "Recuperar cumprimento de tarefa com critério claro e consequência proporcional."
        ),
        "diagnostico": (
            "Confirme se é falta de competência, motivação, clareza de padrão ou contágio "
            "por referência técnica. Use exemplos concretos de OS/turno."
        ),
        "conversa": (
            "SBI objetivo: situação, comportamento observado, impacto em PCM/equipe. "
            "Feche com combinado mensurável e data de revisão."
        ),
        "plano": (
            "1) Feedback 1:1 em 24h. 2) Alinhamento do padrão com a equipe em 3 dias. "
            "3) Auditoria leve por 7 dias com indicador de aderência."
        ),
        "armadilhas": (
            "Discurso genérico de motivação; punir sem ter dado feedback claro; "
            "aceitar 'combinado verbal' sem acompanhamento."
        ),
    },
    "processo": {
        "nome": "Adesão a processo (OS/PCM/procedimento)",
        "foco": (
            "Transformar procedimento em rotina útil, conectada a indicador e segurança operacional."
        ),
        "diagnostico": (
            "Entenda se a resistência é por burocracia percebida, falta de sentido técnico, "
            "pressão de produção ou exemplo ruim de referência."
        ),
        "conversa": (
            "Conecte o procedimento a valor técnico (MTBF, MTTR, retrabalho, peças). "
            "Peça fricções reais e remova 1 burocracia inútil se existir."
        ),
        "plano": (
            "1) Alinhamento técnico do 'porquê' em 48h. 2) Padrão mínimo obrigatório. "
            "3) Auditoria amostral por 7-14 dias com meta de aderência."
        ),
        "armadilhas": (
            "Impor processo sem explicar valor; criar checklist gigante; "
            "cobrar só o referência e liberar o restante."
        ),
    },
    "seguranca": {
        "nome": "Segurança e conformidade",
        "foco": (
            "Proteger vida e conformidade com ação firme, proporcional e documentável."
        ),
        "diagnostico": (
            "Avalie risco imediato, histórico de quase-acidente e influência do exemplo "
            "sobre a equipe. Segurança não é negociável."
        ),
        "conversa": (
            "Seja direto: risco, regra e consequência. Reconheça pressão de produção, "
            "mas deixe claro que procedimento de segurança prevalece. Registre o combinado."
        ),
        "plano": (
            "1) Intervenção imediata (hoje). 2) Reforço do padrão no toolbox em 24-48h. "
            "3) Observação de segurança por 7 dias com registro de desvios."
        ),
        "armadilhas": (
            "Minimizar risco; negociar atalho 'só dessa vez'; feedback só oral em caso grave."
        ),
    },
}


def montar_bloco_playbook(tipo_problema: str) -> str:
    """Retorna bloco de texto para injetar nos prompts dos agentes."""
    pb = PLAYBOOKS_MENTORIA.get((tipo_problema or "").lower())
    if not pb:
        return ""
    return f"""
## Playbook de mentoria ({pb['nome']}):
- Foco: {pb['foco']}
- Guia de diagnóstico: {pb['diagnostico']}
- Guia de conversa: {pb['conversa']}
- Guia de plano: {pb['plano']}
- Armadilhas a evitar: {pb['armadilhas']}

Use o playbook como estrutura-base. Adapte aos fatos do caso; não invente dados.
""".strip()


def nomes_playbooks() -> list[str]:
    return [v["nome"] for v in PLAYBOOKS_MENTORIA.values()]
