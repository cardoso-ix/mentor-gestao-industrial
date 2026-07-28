"""
Casos modelo em 1 clique — preenchem o formulário para demo rápida.
"""

from __future__ import annotations

from dataclasses import dataclass, field

import streamlit as st


@dataclass
class CasoExemplo:
    """Caso pronto para preenchimento rápido do wizard."""

    id: str
    titulo: str
    tipo: str
    situacao: str
    tamanho_equipe: str = ""
    urgencia: str = ""
    contexto_planta: dict[str, str] = field(default_factory=dict)
    detalhes: dict[str, str] = field(default_factory=dict)


CASOS_EXEMPLO: list[CasoExemplo] = [
    CasoExemplo(
        id="os",
        titulo="Resistência a preencher OS",
        tipo="desempenho",
        situacao=(
            "Um técnico sênior da manutenção elétrica se recusa a preencher a ordem de "
            "serviço depois das intervenções. Diz que é perda de tempo. Outros técnicos "
            "começaram a copiar. Já pedi verbalmente duas vezes sem efeito."
        ),
        tamanho_equipe="6-10 técnicos",
        urgencia="Média — resolver esta semana",
        contexto_planta={
            "planta_turno": "elétrica, turno B",
            "clima_equipe": "Tenso",
            "historico_colaborador": "sênior, bom tecnicamente, já orientado 2x",
            "indicador_meta": "% OS preenchidas",
        },
        detalhes={
            "comportamento": "não preenche OS ao finalizar",
            "impacto": "contágio na equipe e perda de histórico",
        },
    ),
    CasoExemplo(
        id="epi",
        titulo="Recusa de EPI / LOTO",
        tipo="seguranca",
        situacao=(
            "Um eletricista experiente insiste em entrar em painel sem LOTO completo. "
            "Alega pressão da produção. Houve quase-acidente na semana passada e isso "
            "já influencia colegas mais novos."
        ),
        tamanho_equipe="6-10 técnicos",
        urgencia="Alta — preciso agir hoje",
        contexto_planta={
            "planta_turno": "elétrica, turno A",
            "clima_equipe": "Há pressão de produção",
            "historico_colaborador": "experiente, referência informal do time",
            "indicador_meta": "desvios de segurança / quase-acidentes",
        },
        detalhes={
            "norma": "LOTO / NR-10",
            "motivo": "produção pressionando prazo",
            "incidente": "quase-acidente na semana passada",
        },
    ),
    CasoExemplo(
        id="turno",
        titulo="Conflito entre turnos",
        tipo="conflito",
        situacao=(
            "O turno A acusa o turno B de deixar equipamentos em mau estado. As passagens "
            "de turno viraram discussão. Já houve atraso em duas intervenções nesta semana."
        ),
        tamanho_equipe="11-20 técnicos",
        urgencia="Média — resolver esta semana",
        contexto_planta={
            "planta_turno": "mecânica, turnos A e B",
            "clima_equipe": "Tenso",
            "historico_colaborador": "atrito recorrente entre as duas equipes",
            "indicador_meta": "atraso de intervenção / retrabalho",
        },
        detalhes={
            "envolvidos": "turnos A e B (mecânica)",
            "duracao": "desde a última parada programada",
            "tentativas": "cobrança informal na passagem de turno",
        },
    ),
    CasoExemplo(
        id="pcm",
        titulo="Resistência a novo PCM",
        tipo="processo",
        situacao=(
            "Implementamos um novo procedimento de PCM. Um técnico veterano diz que o "
            "antigo funcionava melhor. Metade da equipe segue o novo, metade resiste, "
            "e o planejamento perde previsibilidade."
        ),
        tamanho_equipe="6-10 técnicos",
        urgencia="Baixa — posso esperar",
        contexto_planta={
            "planta_turno": "PCM / manutenção geral",
            "clima_equipe": "Tranquilo",
            "historico_colaborador": "veterano, alta influência informal",
            "indicador_meta": "adesão ao plano / backlog",
        },
        detalhes={
            "procedimento": "novo fluxo de PCM",
            "motivo": "acham o processo antigo mais rápido",
            "impacto": "perda de previsibilidade do planejamento",
        },
    ),
    CasoExemplo(
        id="desmotivado",
        titulo="Técnico competente desmotivado",
        tipo="lideranca",
        situacao=(
            "Meu melhor técnico de instrumentação está entregando o mínimo, chegando no "
            "limite do horário e evitando chamados complexos. Antes era referência. "
            "Quero recuperar o engajamento sem perder autoridade."
        ),
        tamanho_equipe="2-5 técnicos",
        urgencia="Média — resolver esta semana",
        contexto_planta={
            "planta_turno": "instrumentação, turno comercial",
            "clima_equipe": "Tranquilo",
            "historico_colaborador": "alta performance anterior, possível desgaste",
            "indicador_meta": "tempo de atendimento / qualidade",
        },
        detalhes={
            "envolvidos": "técnico de instrumentação (referência)",
            "tentativas": "conversa informal rápida",
            "impacto": "equipe perde referência e backlog sobe",
        },
    ),
    CasoExemplo(
        id="passagem",
        titulo="Falha na passagem de turno",
        tipo="comunicacao",
        situacao=(
            "As passagens de turno estão incompletas. O turno seguinte perde tempo "
            "retrabalhando e a equipe reclama que ninguém avisa o status real das OS abertas."
        ),
        tamanho_equipe="6-10 técnicos",
        urgencia="Média — resolver esta semana",
        contexto_planta={
            "planta_turno": "manutenção multiespecialidade",
            "clima_equipe": "Há pressão de produção",
            "historico_colaborador": "problema recorrente entre turnos",
            "indicador_meta": "retrabalho / OS em aberto sem status",
        },
        detalhes={
            "info_faltando": "status real das OS na passagem",
            "envolvidos": "turnos A e B",
            "tentativas": "pedido verbal para 'passar melhor'",
        },
    ),
]


def obter_caso_por_id(caso_id: str) -> CasoExemplo | None:
    for caso in CASOS_EXEMPLO:
        if caso.id == caso_id:
            return caso
    return None


def _aplicar_caso(caso: CasoExemplo) -> None:
    """Preenche o estado do wizard com o caso escolhido."""
    form_key = st.session_state.get("form_key", 0)
    st.session_state.playbook_ativo = caso.id
    st.session_state.tipo_wizard = caso.tipo
    st.session_state.situacao_wizard = caso.situacao
    st.session_state[f"situacao_wizard_{form_key}"] = caso.situacao
    st.session_state.tamanho_wizard = caso.tamanho_equipe
    st.session_state.urgencia_wizard = caso.urgencia
    st.session_state.wizard_respostas = dict(caso.detalhes)
    st.session_state.contexto_planta = dict(caso.contexto_planta)
    # Campos soltos usados pelos widgets
    st.session_state["select_tamanho"] = caso.tamanho_equipe
    st.session_state["select_urgencia"] = caso.urgencia
    st.session_state["ctx_planta_turno"] = caso.contexto_planta.get("planta_turno", "")
    st.session_state["ctx_historico_colaborador"] = caso.contexto_planta.get(
        "historico_colaborador", ""
    )
    st.session_state["ctx_clima_equipe"] = caso.contexto_planta.get("clima_equipe", "")
    st.session_state["ctx_indicador_meta"] = caso.contexto_planta.get("indicador_meta", "")
    for chave, valor in caso.detalhes.items():
        st.session_state[f"wizard_{caso.tipo}_{chave}"] = valor


def renderizar_casos_um_clique() -> None:
    """Grade de casos prontos na área principal."""
    st.markdown(
        '<p class="wizard-secao-titulo">Experimente em 1 clique</p>',
        unsafe_allow_html=True,
    )
    st.caption("Carrega um caso modelo completo. Depois você pode editar e gerar a orientação.")

    cols = st.columns(3)
    for idx, caso in enumerate(CASOS_EXEMPLO):
        with cols[idx % 3]:
            ativo = st.session_state.get("playbook_ativo") == caso.id
            if st.button(
                caso.titulo,
                key=f"caso_exemplo_{caso.id}",
                use_container_width=True,
                type="primary" if ativo else "secondary",
                help=f"Tipo: {caso.tipo}",
            ):
                _aplicar_caso(caso)
                st.rerun()


# Compatibilidade com imports antigos
def renderizar_playbooks_sidebar() -> None:
    """Sidebar opcional com os mesmos casos."""
    st.markdown("#### Casos modelo")
    st.caption("Clique para carregar um exemplo")
    for caso in CASOS_EXEMPLO:
        if st.button(caso.titulo, key=f"playbook_side_{caso.id}", use_container_width=True):
            _aplicar_caso(caso)
            st.rerun()


def obter_playbook_por_id(playbook_id: str) -> CasoExemplo | None:
    return obter_caso_por_id(playbook_id)


# Alias legado
PLAYBOOKS = CASOS_EXEMPLO
