---
name: Mentor de Gestão Industrial
description: Ferramenta de mentoria para supervisores de manutenção industrial
colors:
  primary: "#e67e22"
  primary-bright: "#eb8f3a"
  primary-deep: "#b45309"
  primary-light: "#f8f3ed"
  primary-border: "#e5d0b8"
  ink: "#0f172a"
  ink-secondary: "#1e293b"
  ink-body: "#334155"
  ink-muted: "#5c6b7a"
  ink-caption: "#8a9baa"
  surface: "#ffffff"
  surface-subtle: "#f7f9fb"
  surface-muted: "#eef2f6"
  border: "#d8e0e8"
  hero-from: "#4a2f1a"
  hero-to: "#7a4520"
  hero-muted: "#e8c9a8"
  hero-subtitle: "#f5e6d8"
  complete-bg: "#faefe3"
  complete-ink: "#7a4520"
  complete-border: "#e5c49a"
  confirm-bg: "#faefe3"
  confirm-ink: "#9a4a18"
  confirm-border: "#e5c49a"
  warning-bg: "#faf3eb"
  warning-ink: "#92400e"
  active-bg: "#fdf4ea"
  active-ink: "#9a3412"
  tipo-lideranca: "#6b4423"
  tipo-comunicacao: "#7a4e28"
  tipo-conflito: "#a84832"
  tipo-desempenho: "#c76a2a"
  tipo-processo: "#8b5a32"
  tipo-seguranca: "#8b3a32"
typography:
  body:
    fontFamily: "system-ui, -apple-system, 'Segoe UI', sans-serif"
    fontSize: "1rem"
    fontWeight: 400
    lineHeight: 1.55
  heading-hero:
    fontFamily: "system-ui, -apple-system, 'Segoe UI', sans-serif"
    fontSize: "clamp(1.5rem, 3vw, 2rem)"
    fontWeight: 700
    lineHeight: 1.2
  label-caps:
    fontFamily: "system-ui, -apple-system, 'Segoe UI', sans-serif"
    fontSize: "0.78rem"
    fontWeight: 500
    lineHeight: 1.4
    letterSpacing: "0.04em"
  metric-value:
    fontFamily: "system-ui, -apple-system, 'Segoe UI', sans-serif"
    fontSize: "1.3rem"
    fontWeight: 700
    lineHeight: 1.2
rounded:
  sm: "8px"
  md: "10px"
  lg: "12px"
  xl: "16px"
spacing:
  xs: "0.45rem"
  sm: "0.85rem"
  md: "1.25rem"
  lg: "1.5rem"
  xl: "2rem"
components:
  button-primary:
    backgroundColor: "{colors.primary}"
    textColor: "#ffffff"
    rounded: "{rounded.sm}"
    padding: "0.75rem 1.25rem"
  hero-container:
    backgroundColor: "{colors.hero-from}"
    textColor: "#ffffff"
    rounded: "{rounded.xl}"
    padding: "{spacing.xl} 2.5rem"
  metric-card:
    backgroundColor: "{colors.surface}"
    textColor: "{colors.ink}"
    rounded: "{rounded.lg}"
    padding: "{spacing.md} 1.25rem"
  proximo-passo-card:
    backgroundColor: "{colors.primary-light}"
    textColor: "{colors.ink-secondary}"
    rounded: "{rounded.lg}"
    padding: "1.1rem 1.25rem"
---

## Overview

Interface de produto (Streamlit) com tema claro, acento laranja industrial e hero em azul-marinho. Layout centrado (max-width ~1000px), wizard em etapas e painel de resultados em abas. Visual profissional para ambiente de planta — não marketing, não chatbot.

## Colors

Paleta **restrained** unificada na família **cobre/laranja**: fundos quentes claros, hero em bronze profundo (`#4a2f1a` → `#7a4520`), laranja `#e67e22` para CTA e ênfase. Sem azul marinho — toda a interface conversa com o laranja.

Cores semânticas por tipo de problema (liderança, conflito, etc.) usadas no topo dos cards de métrica (`border-top: 3px`), nunca como faixa lateral grossa.

Contraste mínimo: texto corpo `#334155` sobre `#ffffff` ou `#f8fafc` (≥4.5:1).

## Typography

Família do sistema (`system-ui`, Segoe UI). Sem fontes externas.

- Títulos hero: clamp até 2rem, peso 700
- Corpo: 1rem, line-height 1.55
- Labels de métrica: uppercase pequeno com letter-spacing 0.04em
- Evitar hero/display acima de 2rem neste produto (ferramenta, não landing)

## Elevation

Sombras sutis: cards com `0 1px 6px rgba(15, 23, 42, 0.06)`; hero com `0 8px 28px rgba(15, 45, 74, 0.18)`. Sem glassmorphism. Bordas `1px solid #e2e8f0` para separação de superfícies.

## Components

- **Hero**: gradiente azul, benefícios em chips semitransparentes
- **Wizard**: grid 3 colunas de tipos, formulário em etapas numeradas
- **Métricas**: 3 cards (Tema, Nível, Especialistas)
- **Próximo passo**: card laranja claro com borda de destaque
- **Abas**: Diagnóstico, Estratégia, Conversa, Plano
- **Sidebar**: oculta por padrão, revela no hover (andamento da análise)
- **Botão primário**: gradiente laranja `#f08a2e` → `#e67e22`

## Do's and Don'ts

**Do**
- Manter fundo claro e texto escuro legível
- Usar laranja só para CTA e destaques de prioridade
- Preservar hierarquia wizard → progresso → resultado
- Escrever rótulos em português brasileiro formal

**Don't**
- Dark mode agressivo ou neon estilo gamer
- Gradient text, glassmorphism decorativo, hero-metrics template
- Cards idênticos em grid infinito sem hierarquia
- Eyebrows uppercase em todas as seções
- Faixas `border-left` grossas como único diferencial visual de card (anti-padrão Impeccable)
- Fontes externas que atrasem a abertura sem ganho claro
