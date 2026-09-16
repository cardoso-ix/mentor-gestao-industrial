---
name: Mentor de Gestão Industrial
description: Ferramenta de mentoria para supervisores de manutenção industrial
colors:
  primary: "#d97706"
  primary-bright: "#f59e0b"
  primary-deep: "#b45309"
  primary-light: "#fff7ed"
  primary-border: "#fdba74"
  ink: "#0c0a09"
  ink-secondary: "#1c1917"
  ink-body: "#44403c"
  ink-muted: "#78716c"
  ink-caption: "#a8a29e"
  surface: "#ffffff"
  surface-subtle: "#f5f5f4"
  surface-muted: "#e7e5e4"
  border: "#d6d3d1"
  page-from: "#fafaf9"
  page-to: "#f5f5f4"
  hero-from: "#1c1917"
  hero-to: "#44403c"
  hero-muted: "#fdba74"
  hero-subtitle: "#e7e5e4"
typography:
  display:
    fontFamily: "Space Grotesk, sans-serif"
    fontWeight: 700
  body:
    fontFamily: "DM Sans, sans-serif"
    fontSize: "1rem"
    fontWeight: 400
    lineHeight: 1.6
  heading-hero:
    fontFamily: "Space Grotesk, sans-serif"
    fontSize: "clamp(2rem, 4.8vw, 3.15rem)"
    fontWeight: 700
    lineHeight: 1.05
rounded:
  sm: "6px"
  md: "10px"
  lg: "14px"
  xl: "20px"
spacing:
  xs: "0.5rem"
  sm: "0.85rem"
  md: "1.25rem"
  lg: "1.75rem"
  xl: "2.5rem"
---

## Overview

Interface Streamlit com direção **industrial moderna e executiva**: tipografia expressiva (Space Grotesk + DM Sans), neutros frios, acentos cobre/âmbar (`#f59e0b`/`#d97706`), hero full-bleed de alto contraste e **total responsividade mobile**. Ferramenta projetada para supervisores operarem confortavelmente no computador ou direto no celular/tablet durante rondas no chão de fábrica.

## Colors

- Base: stone frio (`#fafaf9` → `#f5f5f4`)
- Texto: quase preto (`#0c0a09`) e corpo `#44403c`
- Acento/CTA: cobre industrial `#d97706` e âmbar `#f59e0b`
- Hero & Sidebar: grafite profundo `#0c0a09` / `#12100e` / `#1c1917` com trama diagonal sutil e brilho âmbar
- Chips & Badges: vidro fosco com tipografia clara de alto contraste (`#fffbeb` / `#fef08a`)
- Telemetria de Agentes: esmeralda `#10b981` (pulso ativo) e âmbar (varredura laser)

## Typography

- Display/marca/métricas: **Space Grotesk**
- Corpo/briefing: **DM Sans**
- Hierarquia nítida com títulos curtos, balanceados e leitura confortável em telas pequenas

## Layout principles & Mobile-First

- **Mobile-First Responsivo:** Breakpoints dedicados para 768px e 480px; sem transbordamento horizontal (`overflow-x: hidden`), grids com colapso fluído de 1 a 2 colunas.
- **Ergonomia de Toque:** Botões e seletores com altura mínima de 44px-48px para acionamento ágil com uma mão.
- **Sidebar Estável:** Fundo *glassmorphic dark slate* com recolhimento nativo do Streamlit (sem hover acidental que fechava em touchscreens).
- **Agent Telemetry Radar:** HUD de processamento em tempo real com pulso de radar e varredura gradiente durante a mentoria.
- **Ditado de Campo:** Container de áudio (`st.audio_input`) projetado para gravação rápida de ocorrências por voz.
- **Dossiê Executivo:** Deck de KPIs em cards táteis, callout 24h de alta prioridade, roteiro estruturado SBI e checklist interativo de campo.
