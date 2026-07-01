"""
Orquestrador principal do sistema multi-agente.

Coordena o fluxo: RAG → Analista → (Serper se necessário) → agentes especializados → relatório consolidado.
Não é um agente CrewAI — é lógica Python que torna o fluxo previsível e fácil de depurar.
"""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from typing import Callable

from crewai import Crew, Process, Task

import config
from agents.analista import criar_agente_analista, criar_task_analista
from agents.comunicacao import criar_agente_comunicacao, criar_task_comunicacao
from agents.estrategista import criar_agente_estrategista, criar_task_estrategista
from agents.plano_acao import criar_agente_plano_acao, criar_task_plano_acao
from rag import consultar_base, garantir_base_indexada
from tools.serper_search import buscar_web_serper, montar_query_busca


@dataclass
class ResultadoMentoria:
    """Resultado completo de uma análise de situação."""

    analise: dict = field(default_factory=dict)
    estrategia: str = ""
    comunicacao: str = ""
    plano_acao: str = ""
    relatorio_consolidado: str = ""
    contexto_rag: str = ""
    contexto_web: str = ""
    agentes_acionados: list[str] = field(default_factory=list)
    erro: str | None = None


def _limitar_contexto(texto: str, limite: int = 3500) -> str:
    """Evita estourar contexto entre agentes sem cortar no meio de palavra."""
    if not texto or len(texto) <= limite:
        return texto or ""
    corte = texto[:limite].rsplit(" ", 1)[0]
    return (corte or texto[:limite]).rstrip() + "..."


def _validar_chaves() -> str | None:
    """Verifica se as chaves de API obrigatórias estão configuradas."""
    if not config.GROQ_API_KEY:
        return "GROQ_API_KEY não configurada. Adicione no arquivo .env"
    return None


def _extrair_texto_task(saida_crew) -> str:
    """Extrai o texto bruto da saída de um Crew."""
    if hasattr(saida_crew, "tasks_output") and saida_crew.tasks_output:
        task_out = saida_crew.tasks_output[0]
        if hasattr(task_out, "raw") and task_out.raw:
            return str(task_out.raw)
        return str(task_out)
    if hasattr(saida_crew, "raw"):
        return str(saida_crew.raw)
    return str(saida_crew)


def _parsear_analise(saida_crew) -> dict:
    """
    Extrai o JSON da análise do resultado do CrewAI.

    O CrewAI pode retornar pydantic model, dict ou string JSON.
    """
    # Tenta obter do output json da task
    task_out = None
    if hasattr(saida_crew, "tasks_output") and saida_crew.tasks_output:
        task_out = saida_crew.tasks_output[0]

    if task_out is not None:
        if hasattr(task_out, "json_dict") and task_out.json_dict:
            return dict(task_out.json_dict)
        if hasattr(task_out, "pydantic") and task_out.pydantic:
            return task_out.pydantic.model_dump()

    if hasattr(saida_crew, "json_dict") and saida_crew.json_dict:
        return dict(saida_crew.json_dict)

    if hasattr(saida_crew, "pydantic") and saida_crew.pydantic:
        return saida_crew.pydantic.model_dump()

    texto = _extrair_texto_task(saida_crew)

    # Tenta parsear JSON do texto
    try:
        return json.loads(texto)
    except json.JSONDecodeError:
        pass

    # Fallback: extrai JSON entre chaves
    inicio = texto.find("{")
    fim = texto.rfind("}")
    if inicio != -1 and fim != -1:
        try:
            return json.loads(texto[inicio : fim + 1])
        except json.JSONDecodeError:
            pass

    # Último recurso: análise mínima para não quebrar o fluxo
    return {
        "tipo_problema": "lideranca",
        "complexidade": "media",
        "resumo": texto[:300],
        "agentes": ["estrategista", "comunicacao", "plano_acao"],
        "busca_web": False,
        "justificativa": "Análise automática (falha ao parsear JSON)",
    }


def _aplicar_regras_hibridas(analise: dict) -> dict:
    """
    Aplica as regras híbridas de roteamento conforme o plano.

    Garante que Comunicação e Plano entram nos casos esperados,
    mesmo se o LLM esquecer de incluí-los.
    """
    tipo = analise.get("tipo_problema", "").lower()
    complexidade = analise.get("complexidade", "media").lower()
    agentes = set(analise.get("agentes", []))

    tipos_com_comunicacao = {"comunicacao", "conflito", "desempenho", "lideranca"}
    if tipo in tipos_com_comunicacao:
        agentes.add("comunicacao")
        agentes.add("plano_acao")

    if tipo in {"processo", "seguranca"}:
        agentes.add("estrategista")
        agentes.add("plano_acao")
        analise["busca_web"] = True

    if complexidade != "baixa":
        agentes.add("estrategista")

    if complexidade == "baixa" and len(agentes) > 2:
        # Casos triviais: mantém no máximo comunicacao + plano_acao
        pass
    elif complexidade == "baixa":
        agentes.add("plano_acao")

    analise["agentes"] = sorted(agentes)
    return analise


def _montar_relatorio_local(
    analise: dict,
    estrategia: str,
    comunicacao: str,
    plano_acao: str,
) -> str:
    """Síntese executiva para armazenamento (conteúdo das abas fica nos campos próprios)."""
    from ui.text_utils import montar_visao_geral_profissional

    return montar_visao_geral_profissional(analise, plano_acao, estrategia)


def _gerar_relatorio_consolidado(
    situacao: str,
    analise: dict,
    estrategia: str,
    comunicacao: str,
    plano_acao: str,
) -> str:
    """Gera relatório consolidado local (sem LLM extra — mais leve e estável)."""
    return _montar_relatorio_local(analise, estrategia, comunicacao, plano_acao)


def executar_mentoria(
    situacao: str,
    tamanho_equipe: str = "",
    urgencia: str = "",
    categoria_rag: str = "",
    callback_progresso: Callable[[str, float], None] | None = None,
) -> ResultadoMentoria:
    """
    Executa o fluxo completo de mentoria para uma situação.

    Args:
        situacao: Descrição da situação pelo usuário.
        tamanho_equipe: Tamanho da equipe (opcional).
        urgencia: Nível de urgência (opcional).
        categoria_rag: Categoria da base de conhecimento (normas, gestao, processos).
        callback_progresso: Função chamada com (etapa, percentual) para atualizar UI.

    Returns:
        ResultadoMentoria com todas as saídas dos agentes.
    """
    resultado = ResultadoMentoria()

    def progresso(etapa: str, pct: float):
        if callback_progresso:
            callback_progresso(etapa, pct)

    # Validação inicial
    erro_config = _validar_chaves()
    if erro_config:
        resultado.erro = erro_config
        return resultado

    if not situacao.strip():
        resultado.erro = "Descreva a situação antes de analisar."
        return resultado

    try:
        # Indexação RAG só quando o usuário pede análise (não na abertura da página)
        garantir_base_indexada()

        # Etapa 1: Consulta RAG
        progresso("Consultando base de conhecimento...", 0.1)
        resultado.contexto_rag = consultar_base(situacao, categoria=categoria_rag or None)

        # Etapa 2: Agente Analista
        progresso("Analisando situação...", 0.2)
        agente_analista = criar_agente_analista()
        task_analista = criar_task_analista(
            agente_analista,
            situacao,
            tamanho_equipe,
            urgencia,
            contexto_rag=resultado.contexto_rag,
        )
        crew_analista = Crew(
            agents=[agente_analista],
            tasks=[task_analista],
            process=Process.sequential,
            verbose=False,
        )
        saida_analista = crew_analista.kickoff()
        analise = _parsear_analise(saida_analista)
        analise = _aplicar_regras_hibridas(analise)
        resultado.analise = analise
        resultado.agentes_acionados = analise.get("agentes", [])

        # Reconsulta RAG com categoria inferida pelo Analista (se ainda não havia filtro)
        if not categoria_rag:
            mapa_cat = {
                "seguranca": "normas",
                "processo": "processos",
                "lideranca": "gestao",
                "comunicacao": "gestao",
                "conflito": "gestao",
                "desempenho": "gestao",
            }
            cat_inferida = mapa_cat.get(analise.get("tipo_problema", ""), "")
            if cat_inferida:
                ctx_extra = consultar_base(situacao, categoria=cat_inferida)
                if ctx_extra:
                    resultado.contexto_rag = ctx_extra

        # Etapa 3: Busca web (se necessário)
        if analise.get("busca_web"):
            progresso("Buscando referências na web...", 0.3)
            tipo = analise.get("tipo_problema", "processo")
            query = montar_query_busca(situacao, tipo)
            resultado.contexto_web = buscar_web_serper(query)

        agentes = analise.get("agentes", [])
        estrategia_texto = ""
        comunicacao_texto = ""

        # Etapa 4: Agente Estrategista
        if "estrategista" in agentes:
            progresso("Elaborando estratégia de gestão...", 0.45)
            agente_estrategista = criar_agente_estrategista()
            task_estrategista = criar_task_estrategista(
                agente_estrategista,
                situacao,
                analise,
                resultado.contexto_rag,
                resultado.contexto_web,
            )
            crew_estrategista = Crew(
                agents=[agente_estrategista],
                tasks=[task_estrategista],
                process=Process.sequential,
                verbose=False,
            )
            saida = crew_estrategista.kickoff()
            estrategia_texto = _extrair_texto_task(saida)
            resultado.estrategia = estrategia_texto

        # Etapa 5: Agente Comunicação
        if "comunicacao" in agentes:
            progresso("Montando roteiro de comunicação...", 0.65)
            agente_comunicacao = criar_agente_comunicacao()
            task_comunicacao = criar_task_comunicacao(
                agente_comunicacao,
                situacao,
                analise,
                _limitar_contexto(estrategia_texto),
                _limitar_contexto(resultado.contexto_rag, 2000),
            )
            crew_comunicacao = Crew(
                agents=[agente_comunicacao],
                tasks=[task_comunicacao],
                process=Process.sequential,
                verbose=False,
            )
            saida = crew_comunicacao.kickoff()
            comunicacao_texto = _extrair_texto_task(saida)
            resultado.comunicacao = comunicacao_texto

        # Etapa 6: Agente Plano de Ação
        if "plano_acao" in agentes:
            progresso("Criando plano de ação...", 0.8)
            agente_plano = criar_agente_plano_acao()
            task_plano = criar_task_plano_acao(
                agente_plano,
                situacao,
                analise,
                _limitar_contexto(estrategia_texto),
                _limitar_contexto(comunicacao_texto),
                _limitar_contexto(resultado.contexto_rag, 2000),
            )
            crew_plano = Crew(
                agents=[agente_plano],
                tasks=[task_plano],
                process=Process.sequential,
                verbose=False,
            )
            saida = crew_plano.kickoff()
            resultado.plano_acao = _extrair_texto_task(saida)

        # Etapa 7: Relatório consolidado
        progresso("Gerando relatório consolidado...", 0.95)
        resultado.relatorio_consolidado = _gerar_relatorio_consolidado(
            situacao,
            analise,
            resultado.estrategia,
            resultado.comunicacao,
            resultado.plano_acao,
        )

        progresso("Concluído!", 1.0)

    except Exception as exc:
        mensagem = str(exc)
        if "rate_limit" in mensagem.lower() or "429" in mensagem:
            resultado.erro = (
                "Limite de requisições da API Groq atingido. "
                "Aguarde alguns segundos e tente novamente."
            )
        else:
            resultado.erro = f"Erro durante a análise: {mensagem}"

    return resultado
