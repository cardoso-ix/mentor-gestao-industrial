"""
Pacote dos sub-agentes especializados do mentor de gestão industrial.
"""

from agents.analista import criar_agente_analista, criar_task_analista
from agents.comunicacao import criar_agente_comunicacao, criar_task_comunicacao
from agents.estrategista import criar_agente_estrategista, criar_task_estrategista
from agents.plano_acao import criar_agente_plano_acao, criar_task_plano_acao

__all__ = [
    "criar_agente_analista",
    "criar_task_analista",
    "criar_agente_estrategista",
    "criar_task_estrategista",
    "criar_agente_comunicacao",
    "criar_task_comunicacao",
    "criar_agente_plano_acao",
    "criar_task_plano_acao",
]
