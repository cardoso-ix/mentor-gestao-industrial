"""
Gera PDFs resumo para a base de conhecimento (knowledge_base/).

Execute uma vez: python scripts/gerar_pdfs_base.py
"""

from pathlib import Path

from fpdf import FPDF

BASE = Path(__file__).resolve().parent.parent / "knowledge_base"

DOCUMENTOS = {
    "normas/nr06-epi-resumo.pdf": """NR-06 - Equipamentos de Protecao Individual (EPI)

Resumo para gestores de manutenção industrial:

1. O empregador deve fornecer EPI gratuito, adequado ao risco e em perfeito estado.
2. O trabalhador tem obrigacao de usar o EPI fornecido.
3. Recusa injustificada de EPI pode configurar insubordinacao e risco de acidente.
4. O gestor deve registrar orientacoes, treinamentos e advertencias.
5. Quase-acidentes por nao uso de EPI devem ser tratados com feedback imediato.
6. Lider deve dar exemplo no uso de EPI em areas de risco.
7. Substituir EPI danificado e responsabilidade do empregador.

Abordagem recomendada para resistencia:
- Conversa 1:1 com foco em seguranca, nao em punição
- Explicar consequencias reais (acidentes, afastamentos, paradas)
- Envolver equipe na escolha de EPI mais confortavel quando possivel
""",
    "normas/nr10-eletrica-resumo.pdf": """NR-10 - Seguranca em Instalacoes e Servicos em Eletricidade

Pontos-chave para supervisores de manutenção elétrica:

1. Apenas trabalhadores habilitados podem intervir em instalações elétricas.
2. Desenergização, bloqueio e sinalização são obrigatórios quando aplicável.
3. Permissão de Trabalho (PT) e Análise de Risco (APR) em atividades de risco.
4. EPIs específicos: luvas isolantes, capacete, óculos, vestimenta anti-chama.
5. Ferramentas isoladas e detector de tensão antes de intervir.
6. O gestor deve garantir que procedimentos sejam seguidos mesmo sob pressão de produção.

Gestão de equipe:
- Não tolerar atalhos em serviços elétricos
- Reconhecer técnicos que seguem procedimentos
- Investigar causas de pressa (metas, falta de recursos)
""",
    "gestao/lideranca-situacional-resumo.pdf": """Liderança Situacional - Guia para Gestores de Manutenção

Modelo Hersey-Blanchard adaptado ao chão de fábrica:

Estilos de liderança:
1. Diretivo (D1): Para técnico novo ou em tarefa nova - instruções claras, passo a passo
2. Coaching (D2): Para técnico com vontade mas pouca experiência - orientar e ouvir
3. Apoio (D3): Para técnico competente mas desmotivado - menos direção, mais apoio emocional
4. Delegação (D4): Para técnico experiente e motivado - autonomia com metas claras

No contexto de manutenção:
- Técnico veterano resistente a procedimento: pode estar em D3 (competente, baixa motivação)
- Novato em PCM: D1 ou D2
- Melhor técnico desmotivado: D3 - conversa sobre propósito e reconhecimento

Erro comum: tratar todos com o mesmo estilo de liderança.
""",
    "gestao/feedback-sbi-resumo.pdf": """Feedback com Modelo SBI - Situação, Comportamento, Impacto

Estrutura para conversas difíceis com técnicos:

S - Situação: Quando e onde ocorreu (específico)
Exemplo: "Ontem no turno da tarde, durante a parada do compressor C-401"

B - Comportamento: O que foi observado (fato, sem julgamento)
Exemplo: "Você entrou na área sem capacete e disse que seria rápido"

I - Impacto: Consequência para segurança, equipe ou produção
Exemplo: "Isso expõe você a risco de queda de objeto e os colegas passam a achar que a regra não vale"

Perguntas após o feedback:
- O que te levou a fazer assim?
- Como podemos evitar que se repita?
- O que você precisa de mim para seguir o procedimento?

Tom: respeitoso, direto, foco em parceria.
""",
    "processos/ordem-servico-boas-praticas.pdf": """Ordem de Serviço (OS) - Boas Práticas em Manutenção

Por que a OS importa:
1. Rastreabilidade de intervenções e histórico do equipamento
2. Base para indicadores (MTBF, MTTR, custo de manutenção)
3. Segurança: documenta riscos e EPIs necessários
4. Compliance e auditorias

Resistência comum de técnicos:
- "Perda de tempo", "burocracia", "já sei o que fiz"

Como o gestor deve abordar:
- Explicar impacto real (exemplo: falha recorrente sem histórico)
- Simplificar formulário se possível (envolver equipe na revisão)
- Reconhecer quem preenche corretamente
- Meta clara: 100% OS em 2 semanas

Indicador: percentual de OS preenchidas no prazo por técnico.
""",
    "processos/pcm-introducao.pdf": """PCM - Planejamento e Controle da Manutenção

Conceitos para supervisores:

PCM integra: planejamento, programação, execução e controle.

Benefícios:
- Reduz paradas não programadas
- Melhora uso de mão de obra e materiais
- Aumenta confiabilidade dos ativos

Papel do gestor no PCM:
- Garantir aderência aos procedimentos
- Balancear urgências com manutenção planejada
- Comunicar prioridades da semana
- Envolver equipe na melhoria de processos

Resistência a novo PCM:
- Ouvir objeções técnicas (podem ser válidas)
- Pilotar mudança em um equipamento ou área
- Mostrar ganhos mensuráveis em 30 dias
""",
}


def criar_pdf(caminho: Path, texto: str):
    """Cria um PDF simples com o texto fornecido."""
    caminho.parent.mkdir(parents=True, exist_ok=True)
    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()
    pdf.set_font("Helvetica", size=11)
    largura = pdf.epw
    for linha in texto.split("\n"):
        linha_safe = (
            linha.encode("latin-1", errors="replace")
            .decode("latin-1")
            .replace("\t", " ")
        )
        if linha_safe.strip():
            pdf.multi_cell(largura, 6, linha_safe)
        else:
            pdf.ln(4)
    pdf.output(str(caminho))
    print(f"Criado: {caminho.relative_to(BASE.parent)}")


def main():
    for rel_path, conteudo in DOCUMENTOS.items():
        criar_pdf(BASE / rel_path, conteudo)
    print(f"\n{len(DOCUMENTOS)} PDFs gerados em knowledge_base/")


if __name__ == "__main__":
    main()
