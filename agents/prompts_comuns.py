"""Instruções compartilhadas para qualidade das respostas dos agentes."""

REGRAS_QUALIDADE = """
REGRAS OBRIGATÓRIAS DE QUALIDADE:
- Baseie-se APENAS na situação descrita pelo gestor; cite nomes, fatos, prazos e tentativas mencionadas.
- Não invente nomes, eventos, normas ou dados que não foram informados.
- Evite frases genéricas de manual (ex.: "a comunicação é fundamental", "cada caso é único").
- Seja específico para manutenção industrial: turnos, OS, PCM, paradas, equipe técnica, segurança.
- Escreva em português brasileiro formal, claro e profissional.
- Use títulos de seção em linha própria, terminando com dois pontos (ex.: "Diagnóstico estratégico:").
- Use listas com hífen (-) para itens; não use #, **, ### nem outros símbolos markdown.
- Complete todas as frases; não interrompa parágrafos no meio.
"""
