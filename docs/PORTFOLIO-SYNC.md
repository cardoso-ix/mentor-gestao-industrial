# Sync do card no portfólio

Este agente só tem push no repositório `mentor-gestao-industrial`.  
Para atualizar o site [Portifolio](https://github.com/cardoso-ix/Portifolio) e o README do perfil [`cardoso-ix`](https://github.com/cardoso-ix/cardoso-ix), aplique as alterações abaixo (ou rode um agente com acesso a esses repos).

## Objetivo

Deixar o Mentor fácil de testar: CTA **Demo** visível, stack correta (**OpenCode Go · DeepSeek V4 Flash · CrewAI · RAG · Streamlit**) e links oficiais.

## Links canônicos

| Uso | URL |
|-----|-----|
| Demo (página HF) | https://huggingface.co/spaces/duzinxd/mentor-gestao-industrial |
| App direto | https://duzinxd-mentor-gestao-industrial.hf.space |
| GitHub | https://github.com/cardoso-ix/mentor-gestao-industrial |

---

## 1) `Portifolio/index.html` — card do Mentor

Substitua o bloco do card por:

```html
            <article class="project-card project-card--compact fade-in">
              <div class="project-card__image">
                <img src="assets/images/mentor-gestao-preview.png?v=6" alt="Preview do Mentor de Gestão Industrial" class="project-card__thumb" width="640" height="360" loading="lazy">
              </div>
              <div class="project-card__body">
                <h3 class="project-card__title">Mentor de Gestão Industrial</h3>
                <p class="project-card__lead">Demo pública: briefing executivo para supervisores de manutenção — diagnóstico, conversa SBI e plano 24h. Clique em Demo para testar.</p>
                <p class="project-card__note">CrewAI · OpenCode Go · DeepSeek V4 Flash · RAG · Streamlit</p>
                <div class="project-card__links">
                  <a href="https://huggingface.co/spaces/duzinxd/mentor-gestao-industrial" class="project-card__link" target="_blank" rel="noopener noreferrer">Testar demo</a>
                  <a href="https://github.com/cardoso-ix/mentor-gestao-industrial" class="project-card__link" target="_blank" rel="noopener noreferrer">GitHub</a>
                </div>
              </div>
            </article>
```

Sugestão: se quiser destaque máximo, mova este card para `project-card--featured` (no lugar ou ao lado da Automação LinkedIn).

Bump do CSS se houver cache: `css/style.css?v=34` no `<head>`.

---

## 2) `Portifolio/README.md`

Linha da tabela de projetos:

```md
| Mentor de Gestão Industrial | [Demo](https://huggingface.co/spaces/duzinxd/mentor-gestao-industrial) | [GitHub](https://github.com/cardoso-ix/mentor-gestao-industrial) — CrewAI · OpenCode Go · DeepSeek V4 Flash · RAG |
```

---

## 3) `Portifolio/docs/PROJETOS-GITHUB.md`

Atualizar a linha da tabela e a seção **3) mentor-gestao-industrial**:

- Stack: `CrewAI · OpenCode Go (DeepSeek V4 Flash) · RAG · ChromaDB · Streamlit`
- Demo: https://huggingface.co/spaces/duzinxd/mentor-gestao-industrial
- Remover menções a Groq / OpenRouter Gemma como stack atual
- Description GitHub: alinhar ao texto do README do Mentor (sem Groq)

---

## 4) `Portifolio/docs/LINKEDIN-PERFIL.md`

Trocar a linha do Mentor para:

```text
• Mentor de Gestão Industrial — multi-agente CrewAI + OpenCode Go (DeepSeek V4 Flash) + RAG (demo no Hugging Face)
```

Featured: manter link https://huggingface.co/spaces/duzinxd/mentor-gestao-industrial

---

## 5) README do perfil `cardoso-ix/cardoso-ix`

```md
| [**Mentor de Gestão Industrial**](https://github.com/cardoso-ix/mentor-gestao-industrial) | Multi-agente (CrewAI + OpenCode Go / DeepSeek V4 Flash + RAG) para supervisores de manutenção | [▶ Testar demo](https://huggingface.co/spaces/duzinxd/mentor-gestao-industrial) |
```

Stack sugerida: trocar `Groq` por `OpenCode Go` / `DeepSeek`.

---

## 6) Metadados do repo Mentor (manual no GitHub UI)

**Description:**  
`Mentor multi-agente para supervisores de manutenção — CrewAI, OpenCode Go (DeepSeek V4 Flash), RAG, Streamlit. Demo pública no Hugging Face.`

**Website:** https://huggingface.co/spaces/duzinxd/mentor-gestao-industrial  

**Topics sugeridos:** `crewai`, `streamlit`, `rag`, `chromadb`, `opencode`, `deepseek`, `manutencao`, `huggingface-spaces`
