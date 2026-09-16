"""Estilos CSS — layout industrial moderno (claro, tipografia expressiva)."""

CSS_APP = """
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:ital,opsz,wght@0,9..40,400;0,9..40,500;0,9..40,600;0,9..40,700;1,9..40,400&family=Space+Grotesk:wght@500;600;700&display=swap');

:root {
    /* Acento — cobre industrial (marca) */
    --color-primary: #d97706;
    --color-primary-bright: #f59e0b;
    --color-primary-deep: #b45309;
    --color-primary-light: #fff7ed;
    --color-primary-border: #fdba74;

    /* Hero — grafite quente (atmosfera de planta, sem dark mode) */
    --color-hero-from: #1c1917;
    --color-hero-to: #44403c;
    --color-hero-muted: #fdba74;
    --color-hero-subtitle: #e7e5e4;

    /* Neutros frios — base moderna */
    --color-ink: #0c0a09;
    --color-ink-secondary: #1c1917;
    --color-ink-body: #44403c;
    --color-ink-muted: #78716c;
    --color-ink-caption: #a8a29e;
    --color-surface: #ffffff;
    --color-surface-subtle: #f5f5f4;
    --color-surface-muted: #e7e5e4;
    --color-border: #d6d3d1;
    --color-page-from: #fafaf9;
    --color-page-to: #f5f5f4;

    --color-complete-bg: #ecfdf5;
    --color-complete-ink: #047857;
    --color-complete-border: #a7f3d0;
    --color-success-bg: var(--color-complete-bg);
    --color-success-ink: var(--color-complete-ink);
    --color-success-border: var(--color-complete-border);

    --color-warning-bg: #fffbeb;
    --color-warning-ink: #92400e;
    --color-warning-border: #fde68a;
    --color-active-bg: #fff7ed;
    --color-active-ink: #9a3412;
    --color-active-border: #fdba74;

    --color-confirm-bg: #fff7ed;
    --color-confirm-ink: #9a3412;
    --color-confirm-border: #fdba74;

    --color-error-bg: #fef2f2;
    --color-error-ink: #991b1b;
    --color-error-border: #fecaca;
    --color-info-bg: #f5f5f4;
    --color-info-ink: #44403c;
    --color-info-border: #d6d3d1;

    --color-tipo-lideranca: #57534e;
    --color-tipo-comunicacao: #78716c;
    --color-tipo-conflito: #b45309;
    --color-tipo-desempenho: #d97706;
    --color-tipo-processo: #57534e;
    --color-tipo-seguranca: #9a3412;
    --color-tipo-default: var(--color-ink-caption);

    --font-display: "Space Grotesk", "Segoe UI", sans-serif;
    --font-body: "DM Sans", "Segoe UI", sans-serif;

    --radius-sm: 6px;
    --radius-md: 10px;
    --radius-lg: 14px;
    --radius-xl: 20px;
    --space-xs: 0.5rem;
    --space-sm: 0.85rem;
    --space-md: 1.25rem;
    --space-lg: 1.75rem;
    --space-xl: 2.5rem;
    --shadow-sm: 0 1px 2px rgba(12, 10, 9, 0.04);
    --shadow-md: 0 10px 30px rgba(12, 10, 9, 0.08);
    --ease-out: cubic-bezier(0.22, 1, 0.36, 1);
    --ease-out-quart: cubic-bezier(0.25, 1, 0.5, 1);
    --ease-out-expo: cubic-bezier(0.16, 1, 0.3, 1);
    --dur-instant: 120ms;
    --dur-fast: 180ms;
    --dur-normal: 260ms;
    --dur-moderate: 360ms;
}

html, body, [class*="css"] {
    font-family: var(--font-body) !important;
    -webkit-font-smoothing: antialiased;
}

.stApp {
    background:
        radial-gradient(1200px 500px at 10% -10%, rgba(217, 119, 6, 0.08), transparent 55%),
        radial-gradient(900px 420px at 95% 5%, rgba(68, 64, 60, 0.06), transparent 50%),
        linear-gradient(180deg, var(--color-page-from) 0%, var(--color-page-to) 100%) !important;
    color: var(--color-ink);
    line-height: 1.6;
}

header[data-testid="stHeader"] {
    background: rgba(250, 250, 249, 0.85) !important;
    backdrop-filter: blur(8px);
    border-bottom: 1px solid transparent !important;
}
div[data-testid="stDecoration"] {
    background: transparent !important;
    background-image: none !important;
}

.main .block-container {
    padding-top: 0.75rem !important;
    padding-bottom: 3rem !important;
    max-width: 1080px;
}

.stApp h1, .stApp h2, .stApp h3 {
    font-family: var(--font-display) !important;
    color: var(--color-ink) !important;
    letter-spacing: -0.02em;
}
.stApp h4, .stApp h5, .stApp h6 { color: var(--color-ink-secondary) !important; }
.stApp p, .stApp li { color: var(--color-ink-body) !important; max-width: 70ch; }
.stApp label { color: var(--color-ink-muted) !important; font-weight: 500 !important; }
.stApp .stCaption { color: var(--color-ink-muted) !important; }

/* Hero full-bleed — contraste alto (vence .stApp p/h1) */
.hero-bleed {
    position: relative;
    left: 50%;
    right: 50%;
    margin-left: -50vw;
    margin-right: -50vw;
    width: 100vw;
    margin-bottom: 1.75rem;
    overflow: hidden;
    isolation: isolate;
    color-scheme: dark;
    background:
        linear-gradient(115deg, #0c0a09 0%, #1c1917 42%, #292524 72%, #7c2d12 120%);
    animation: hero-entra var(--dur-moderate) var(--ease-out-expo) both;
}
.hero-bleed span,
.hero-bleed p,
.hero-bleed strong,
.hero-bleed div {
    color: #e7e5e4;
}
.hero-glow {
    position: absolute;
    right: -8%;
    top: -35%;
    width: min(58vw, 620px);
    height: min(58vw, 620px);
    border-radius: 50%;
    background: radial-gradient(circle, rgba(245, 158, 11, 0.28) 0%, rgba(217, 119, 6, 0.08) 42%, transparent 70%);
    pointer-events: none;
    z-index: 0;
}
.hero-grid {
    position: absolute;
    inset: 0;
    background-image:
        linear-gradient(rgba(255,255,255,0.045) 1px, transparent 1px),
        linear-gradient(90deg, rgba(255,255,255,0.045) 1px, transparent 1px);
    background-size: 48px 48px;
    mask-image: linear-gradient(120deg, transparent 10%, rgba(0,0,0,0.55) 45%, rgba(0,0,0,0.2) 100%);
    pointer-events: none;
    z-index: 0;
}
.hero-bleed::after {
    content: "";
    position: absolute;
    inset: auto 0 0 0;
    height: 56px;
    background: linear-gradient(180deg, transparent, var(--color-page-from));
    pointer-events: none;
    z-index: 2;
}
.hero-inner {
    position: relative;
    z-index: 1;
    max-width: 1080px;
    margin: 0 auto;
    padding: clamp(2.6rem, 6vw, 4.2rem) 1.5rem clamp(3rem, 6vw, 4.4rem);
    display: grid;
    grid-template-columns: minmax(0, 1.35fr) minmax(0, 0.85fr);
    gap: clamp(1.5rem, 4vw, 3rem);
    align-items: end;
}
.hero-copy { max-width: 34rem; }
.stApp .hero-bleed .hero-kicker,
.hero-bleed .hero-kicker {
    color: #fdba74 !important;
    font-size: 0.8rem !important;
    font-weight: 650 !important;
    letter-spacing: 0.14em !important;
    text-transform: uppercase !important;
    margin: 0 0 0.85rem 0 !important;
    max-width: none !important;
}
.stApp .hero-bleed .hero-brand,
.hero-bleed .hero-brand,
.stApp h1.hero-brand {
    font-family: var(--font-display) !important;
    color: #ffffff !important;
    font-size: clamp(2.35rem, 5.4vw, 3.55rem) !important;
    font-weight: 700 !important;
    letter-spacing: -0.04em !important;
    line-height: 0.98 !important;
    margin: 0 0 1rem 0 !important;
    max-width: 11ch !important;
    text-wrap: balance;
}
.stApp .hero-bleed .hero-lede,
.hero-bleed .hero-lede {
    color: #e7e5e4 !important;
    font-size: clamp(1.02rem, 1.6vw, 1.18rem) !important;
    line-height: 1.55 !important;
    margin: 0 0 1.35rem 0 !important;
    max-width: 36ch !important;
    font-weight: 400 !important;
}
.stApp .hero-bleed .hero-cta-hint,
.hero-bleed .hero-cta-hint {
    display: inline-flex;
    align-items: center;
    gap: 0.45rem;
    color: #ffffff !important;
    font-size: 0.92rem !important;
    font-weight: 600 !important;
    margin: 0 !important;
    max-width: none !important;
    opacity: 0.92;
}
.hero-cta-hint::after {
    content: "↓";
    color: #f59e0b;
    font-size: 1rem;
    animation: hint-bounce 1.6s var(--ease-out) infinite;
}
.hero-aside {
    display: flex;
    flex-direction: column;
    gap: 0.7rem;
    justify-content: flex-end;
    padding-bottom: 0.25rem;
    border-left: 1px solid rgba(255, 255, 255, 0.14);
    padding-left: 1.35rem;
}
.hero-aside__label {
    font-size: 0.72rem !important;
    font-weight: 650 !important;
    letter-spacing: 0.12em !important;
    text-transform: uppercase !important;
    color: rgba(253, 186, 116, 0.9) !important;
    margin: 0 0 0.35rem 0 !important;
    max-width: none !important;
}
.hero-aside__item {
    font-family: var(--font-display);
    color: rgba(255, 255, 255, 0.78);
    font-size: clamp(1.2rem, 2.2vw, 1.55rem);
    font-weight: 600;
    letter-spacing: -0.03em;
    line-height: 1.15;
}
.hero-aside__item:nth-child(2) { color: #ffffff; }
.hero-aside__item:nth-child(3) { color: rgba(255, 255, 255, 0.78); }
.hero-aside__item:nth-child(4) { color: #fdba74; }

/* Nota geral — caracterização profissional do produto */
.nota-geral {
    display: grid;
    grid-template-columns: auto 1fr;
    gap: 0.85rem 1.25rem;
    align-items: start;
    margin: 0 0 1.65rem 0;
    padding: 0.15rem 0 1.25rem;
    border-bottom: 1px solid var(--color-border);
    animation: nota-geral-entra var(--dur-moderate) var(--ease-out-expo) both;
}
.nota-geral__rotulo {
    font-family: var(--font-display) !important;
    font-size: 0.72rem !important;
    font-weight: 700 !important;
    letter-spacing: 0.1em !important;
    text-transform: uppercase !important;
    color: var(--color-primary-deep) !important;
    margin: 0.15rem 0 0 0 !important;
    max-width: none !important;
    white-space: nowrap;
}
.nota-geral__texto {
    color: var(--color-ink-body) !important;
    font-size: 0.95rem !important;
    line-height: 1.55 !important;
    margin: 0 !important;
    max-width: 68ch !important;
}
.nota-geral__texto strong {
    color: var(--color-ink) !important;
    font-weight: 650 !important;
}

/* Intro do wizard */
.wizard-intro {
    margin: 0 0 1.1rem 0;
}
.wizard-intro__titulo {
    font-family: var(--font-display) !important;
    color: var(--color-ink) !important;
    font-size: clamp(1.2rem, 2vw, 1.4rem) !important;
    font-weight: 700 !important;
    letter-spacing: -0.03em !important;
    margin: 0 0 0.35rem 0 !important;
}
.wizard-intro__texto {
    color: var(--color-ink-muted) !important;
    font-size: 0.95rem !important;
    margin: 0 !important;
    max-width: 52ch !important;
}

.sidebar-brand {
    margin: 0 0 1rem 0;
    padding-bottom: 0.85rem;
    border-bottom: 1px solid var(--color-border);
}
.sidebar-brand__nome {
    font-family: var(--font-display) !important;
    font-size: 1.05rem !important;
    font-weight: 700 !important;
    letter-spacing: -0.02em !important;
    color: var(--color-ink) !important;
    margin: 0 0 0.2rem 0 !important;
    max-width: none !important;
}
.sidebar-brand__desc {
    font-size: 0.8rem !important;
    color: var(--color-ink-muted) !important;
    margin: 0 !important;
    max-width: none !important;
    line-height: 1.4 !important;
}

.resultado-nota {
    color: var(--color-ink-muted) !important;
    font-size: 0.88rem !important;
    line-height: 1.45 !important;
    margin: 0 0 0.85rem 0 !important;
    max-width: 62ch !important;
}
.section-heading--inline {
    border-bottom: none !important;
    padding-bottom: 0 !important;
    margin-bottom: 0.45rem !important;
    font-size: 0.78rem !important;
    text-transform: uppercase;
    letter-spacing: 0.07em !important;
    color: var(--color-ink-caption) !important;
    font-weight: 700 !important;
}

.secao-resultado-sep {
    height: 1px;
    background: linear-gradient(90deg, transparent, var(--color-border) 12%, var(--color-border) 88%, transparent);
    margin: 1.75rem 0 1.25rem;
}

/* Compatibilidade com markup antigo */
.hero-container {
    background: transparent;
    border: none;
    box-shadow: none;
    padding: 0;
    margin: 0;
}
.hero-container .hero-title { display: none; }
.hero-container .hero-eyebrow { display: none; }
.hero-container .hero-subtitle { display: none; }
.hero-accent-line { display: none; }

/* Fluxo — passos do wizard (trilho moderno) */
.fluxo-passos {
    display: grid;
    grid-template-columns: repeat(3, minmax(0, 1fr));
    gap: 0.65rem;
    margin-bottom: var(--space-lg);
}
.fluxo-passo {
    display: flex;
    align-items: center;
    gap: 0.65rem;
    padding: 0.7rem 0.85rem;
    border-radius: var(--radius-md);
    border: 1px solid transparent;
    background: transparent;
    font-size: 0.84rem;
    color: var(--color-ink-muted);
    transition:
        background var(--dur-fast) var(--ease-out-quart),
        border-color var(--dur-fast) var(--ease-out-quart),
        color var(--dur-fast) var(--ease-out-quart);
}
.fluxo-passo--active {
    background: var(--color-surface);
    border-color: var(--color-border);
    color: var(--color-ink);
    box-shadow: var(--shadow-sm);
}
.fluxo-passo--done {
    background: transparent;
    border-color: transparent;
    color: var(--color-complete-ink);
}
.fluxo-passo--pending { opacity: 0.55; }
.fluxo-passo__num {
    display: inline-flex;
    align-items: center;
    justify-content: center;
    width: 1.5rem;
    height: 1.5rem;
    border-radius: 6px;
    font-family: var(--font-display);
    font-size: 0.75rem;
    font-weight: 700;
    background: var(--color-surface-muted);
    color: var(--color-ink-secondary);
    flex-shrink: 0;
}
.fluxo-passo--active .fluxo-passo__num {
    background: var(--color-primary);
    color: #fff;
    animation: pulso-indicador var(--dur-moderate) var(--ease-out-expo);
}
.fluxo-passo--done .fluxo-passo__num {
    background: var(--color-complete-ink);
    color: #fff;
}
.fluxo-passo__label {
    font-weight: 560;
    line-height: 1.3;
    font-family: var(--font-display);
    letter-spacing: -0.01em;
}

/* Wizard — superfície limpa, sem caixa pesada */
.wizard-panel-marker { display: none; }
.wizard-panel-marker + div[data-testid="stVerticalBlockBorderWrapper"] {
    background: transparent !important;
    border: none !important;
    border-radius: 0 !important;
    padding: 0 !important;
    margin-bottom: var(--space-md) !important;
    box-shadow: none !important;
}
.wizard-secao-titulo {
    font-family: var(--font-display) !important;
    color: var(--color-ink) !important;
    font-size: 1.15rem !important;
    font-weight: 650 !important;
    letter-spacing: -0.02em !important;
    margin: 1.6rem 0 0.95rem 0 !important;
    padding: 0 !important;
    border: none !important;
}
.wizard-tipo-desc {
    background: transparent;
    border: none;
    border-left: 2px solid var(--color-primary);
    border-radius: 0;
    padding: 0.15rem 0 0.15rem 0.85rem;
    font-size: 0.92rem;
    color: var(--color-ink-body);
    margin: 0.55rem 0 1.1rem;
}
.wizard-divider {
    height: 1px;
    background: var(--color-border);
    margin: 1.25rem 0 1.5rem;
    opacity: 0.85;
}
.wizard-acoes-hint {
    margin: 1.25rem 0 0.65rem;
    font-size: 0.92rem;
    color: var(--color-ink-muted);
    font-weight: 500;
}
.wizard-hint {
    background: var(--color-surface);
    border: 1px dashed var(--color-border);
    border-radius: var(--radius-md);
    padding: var(--space-md);
    color: var(--color-ink-muted);
    font-size: 0.92rem;
    margin: 0.5rem 0 1rem;
}

/* Meta strip (substitui cards de métrica) */
.resultado-meta {
    display: flex;
    flex-wrap: wrap;
    gap: 0.6rem 1.25rem;
    padding: 0.2rem 0 0.85rem;
    margin-bottom: 0.35rem;
    border-bottom: 1px solid var(--color-border);
    animation: painel-progresso-entra var(--dur-normal) var(--ease-out-quart) both;
}
.resultado-meta__item {
    display: flex;
    flex-direction: column;
    gap: 0.15rem;
    min-width: 7rem;
}
.resultado-meta__label {
    font-size: 0.72rem;
    font-weight: 600;
    letter-spacing: 0.06em;
    text-transform: uppercase;
    color: var(--color-ink-caption) !important;
    margin: 0 !important;
}
.resultado-meta__value {
    font-family: var(--font-display) !important;
    font-size: 1.15rem !important;
    font-weight: 650 !important;
    color: var(--color-ink) !important;
    margin: 0 !important;
    letter-spacing: -0.02em;
}

/* Legacy metric-card → strip-like */
.metric-card {
    background: transparent;
    border: none;
    border-top: none;
    border-radius: 0;
    padding: 0.2rem 0;
    text-align: left;
    box-shadow: none;
    min-height: auto;
}
.metric-card:hover { transform: none; box-shadow: none; }
.metric-card h4 {
    color: var(--color-ink-caption);
    font-size: 0.72rem;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.06em;
    margin: 0;
}
.metric-card p {
    font-family: var(--font-display) !important;
    color: var(--color-ink) !important;
    font-size: 1.15rem;
    font-weight: 650;
    margin: 0.2rem 0 0 0;
    max-width: none !important;
    letter-spacing: -0.02em;
}

.resultado-banner { display: none; }

.resultado-shell-marker { display: none; }
.resultado-shell-marker + div[data-testid="stVerticalBlockBorderWrapper"] {
    background: var(--color-surface) !important;
    border: 1px solid var(--color-border) !important;
    border-radius: var(--radius-lg) !important;
    padding: clamp(1rem, 2vw, 1.45rem) !important;
    margin-top: var(--space-sm) !important;
    margin-bottom: var(--space-sm) !important;
    box-shadow: var(--shadow-sm) !important;
    animation: resultado-entra var(--dur-moderate) var(--ease-out-expo) both;
}
.resultado-shell__header {
    display: flex;
    flex-wrap: wrap;
    align-items: baseline;
    justify-content: space-between;
    gap: 0.4rem;
    margin-bottom: 0.75rem;
}
.resultado-shell__titulo {
    font-family: var(--font-display) !important;
    color: var(--color-ink) !important;
    font-size: clamp(1.15rem, 1.8vw, 1.35rem) !important;
    font-weight: 700 !important;
    letter-spacing: -0.03em !important;
    margin: 0 !important;
}
.resultado-shell__meta {
    font-size: 0.8rem;
    color: var(--color-ink-caption);
}

.progresso-painel {
    background: var(--color-surface);
    border: 1px solid var(--color-border);
    border-radius: var(--radius-xl);
    padding: var(--space-lg);
    margin: var(--space-md) 0;
    box-shadow: var(--shadow-sm);
    animation: painel-progresso-entra var(--dur-normal) var(--ease-out-quart) both;
}
.progresso-painel__titulo {
    font-family: var(--font-display) !important;
    color: var(--color-ink) !important;
    font-size: 1.1rem !important;
    font-weight: 650 !important;
    letter-spacing: -0.02em !important;
    margin: 0 0 0.35rem 0 !important;
}
.progresso-painel__etapa {
    color: var(--color-ink-body) !important;
    font-size: 0.95rem !important;
    margin: 0 0 0.25rem 0 !important;
}
.progresso-painel__pct {
    color: var(--color-ink-caption) !important;
    font-size: 0.78rem !important;
    margin: 0 0 0.75rem 0 !important;
}

.timeline-horizontal {
    display: flex;
    gap: 0.4rem;
    margin-top: var(--space-sm);
    flex-wrap: wrap;
}
.timeline-h-item {
    flex: 1;
    min-width: 72px;
    text-align: center;
    padding: 0.55rem 0.4rem;
    border-radius: var(--radius-md);
    font-size: 0.72rem;
    border: 1px solid transparent;
    transition:
        background var(--dur-fast) var(--ease-out-quart),
        border-color var(--dur-fast) var(--ease-out-quart),
        color var(--dur-fast) var(--ease-out-quart);
}
.timeline-h-icon { display: block; font-size: 0.85rem; margin-bottom: 0.15rem; }
.timeline-h-label { display: block; line-height: 1.25; font-weight: 500; }
.timeline-h-item.timeline-active {
    animation: etapa-ativa-pulso 0.42s var(--ease-out-expo);
}
.timeline-h-item.timeline-done {
    background: var(--color-complete-bg);
    color: var(--color-complete-ink);
    border-color: var(--color-complete-border);
}

.alerta {
    border-radius: var(--radius-md);
    padding: 0.8rem 0.95rem;
    font-size: 0.9rem;
    line-height: 1.45;
    margin: 0.5rem 0;
}
.alerta--erro { background: var(--color-error-bg); border: 1px solid var(--color-error-border); color: var(--color-error-ink); }
.alerta--aviso { background: var(--color-warning-bg); border: 1px solid var(--color-warning-border); color: var(--color-warning-ink); }
.alerta--info { background: var(--color-info-bg); border: 1px solid var(--color-info-border); color: var(--color-info-ink); }

.proximo-passo-card {
    background: transparent;
    border: none;
    border-left: 3px solid var(--color-primary);
    border-radius: 0;
    padding: 0.1rem 0 0.1rem 0.9rem;
    margin: 0.85rem 0 1rem;
    color: var(--color-ink-secondary);
    line-height: 1.5;
    box-shadow: none;
}
.proximo-passo-card:hover { box-shadow: none; }
.proximo-passo-card strong {
    display: block;
    color: var(--color-primary-deep);
    font-size: 0.72rem;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.07em;
    margin-bottom: 0.45rem;
}
.proximo-passo-card p {
    margin: 0 !important;
    color: var(--color-ink) !important;
    font-size: 1.02rem !important;
    max-width: 62ch !important;
    font-family: var(--font-display) !important;
    font-weight: 520 !important;
    letter-spacing: -0.015em;
}

.section-heading {
    font-family: var(--font-display) !important;
    color: var(--color-ink) !important;
    font-size: 1.05rem !important;
    font-weight: 650 !important;
    letter-spacing: -0.02em !important;
    margin: 0 0 0.85rem 0 !important;
    padding-bottom: 0.4rem;
    border-bottom: 1px solid var(--color-border);
}

.timeline-step {
    padding: var(--space-xs) var(--space-sm);
    border-radius: var(--radius-sm);
    margin: 0.2rem 0;
    font-size: 0.85rem;
    border: 1px solid transparent;
}
.timeline-done { background: var(--color-complete-bg); color: var(--color-complete-ink); border-color: var(--color-complete-border); }
.timeline-active {
    background: var(--color-active-bg);
    color: var(--color-active-ink);
    font-weight: 600;
    border-color: var(--color-active-border);
}
.timeline-pending { background: var(--color-surface-muted); color: var(--color-ink-caption); }

.aviso-publico {
    background: transparent;
    color: var(--color-ink-body);
    border: none;
    border-left: 2px solid var(--color-primary);
    padding: 0.15rem 0 0.15rem 0.85rem;
    border-radius: 0;
    font-size: 0.82rem;
    line-height: 1.45;
}
.aviso-publico strong {
    color: var(--color-ink);
    font-weight: 650;
}

.rodape-app {
    width: 100%;
    margin-top: var(--space-xl);
}
.rodape-app__inner {
    border-top: 1px solid var(--color-border);
    padding: var(--space-lg) 0 var(--space-md);
    text-align: center;
}
.rodape-app__linha {
    font-size: 0.8rem !important;
    color: var(--color-ink-muted) !important;
    margin: 0 auto 0.35rem !important;
    max-width: none !important;
}
.rodape-app__linha--muted {
    font-size: 0.74rem !important;
    color: var(--color-ink-caption) !important;
    margin: 0 auto !important;
}
.rodape-copy {
    font-size: 0.78rem;
    color: var(--color-ink-caption) !important;
    text-align: center !important;
    width: 100% !important;
    max-width: none !important;
    display: block !important;
    margin: var(--space-xl) auto 0 !important;
    padding: var(--space-md) 0 var(--space-lg) !important;
    border-top: 1px solid var(--color-border);
}

/* Sidebar — Glassmorphic industrial estável e responsivo (sem hover-slide frágil) */
section[data-testid="stSidebar"] {
    background: #12100e !important;
    border-right: 1px solid rgba(253, 186, 116, 0.15) !important;
    box-shadow: 4px 0 24px rgba(0, 0, 0, 0.25) !important;
    backdrop-filter: blur(12px) !important;
}
section[data-testid="stSidebar"] > div,
div[data-testid="stSidebarContent"] {
    background: #12100e !important;
    color: #e7e5e4 !important;
    padding-top: 1rem !important;
}
section[data-testid="stSidebar"] p,
section[data-testid="stSidebar"] span,
section[data-testid="stSidebar"] label,
section[data-testid="stSidebar"] .stCaption {
    color: #d6d3d1 !important;
}
section[data-testid="stSidebar"] h1,
section[data-testid="stSidebar"] h2,
section[data-testid="stSidebar"] h3,
section[data-testid="stSidebar"] h4 {
    color: #ffffff !important;
    font-family: var(--font-display) !important;
}
section[data-testid="stSidebar"] .sidebar-brand {
    border-bottom: 1px solid rgba(255, 255, 255, 0.1) !important;
}
section[data-testid="stSidebar"] .sidebar-brand__nome {
    color: #ffffff !important;
}
section[data-testid="stSidebar"] .sidebar-brand__desc {
    color: #fdba74 !important;
}
/* Botão de colapso da sidebar */
[data-testid="stSidebarCollapseButton"] button {
    color: #fdba74 !important;
    background: rgba(255, 255, 255, 0.05) !important;
    border-radius: var(--radius-sm) !important;
}
[data-testid="stSidebarCollapseButton"] button:hover {
    background: rgba(245, 158, 11, 0.15) !important;
    color: #ffffff !important;
}

.stTabs [data-baseweb="tab-list"] {
    border-bottom: 1px solid var(--color-border);
    gap: 0.15rem;
}
.stTabs [data-baseweb="tab"] {
    color: var(--color-ink-muted) !important;
    font-weight: 500 !important;
    font-family: var(--font-display) !important;
    padding: 0.65rem 0.95rem !important;
}
.stTabs [aria-selected="true"] {
    color: var(--color-ink) !important;
    border-bottom: 2px solid var(--color-primary) !important;
    background: transparent !important;
    font-weight: 650 !important;
}
.stTabs [data-baseweb="tab-panel"] {
    padding-top: var(--space-md) !important;
    animation: painel-aba-entra var(--dur-normal) var(--ease-out-quart) both;
}

div[data-testid="stExpander"] {
    background: transparent !important;
    border: none !important;
    border-top: 1px solid var(--color-border) !important;
    border-radius: 0 !important;
    padding-top: 0.35rem !important;
}
div[data-testid="stExpander"]:focus-within {
    border-color: var(--color-primary-border) !important;
    box-shadow: none !important;
}

.stButton > button {
    border-radius: var(--radius-sm) !important;
    min-height: 2.85rem;
    font-family: var(--font-display) !important;
    letter-spacing: -0.01em !important;
    transition:
        background var(--dur-fast) var(--ease-out-quart),
        box-shadow var(--dur-fast) var(--ease-out-quart),
        transform var(--dur-instant) var(--ease-out-expo),
        border-color var(--dur-fast) var(--ease-out-quart),
        color var(--dur-fast) var(--ease-out-quart) !important;
}
.stButton > button[kind="primary"] {
    background: var(--color-primary) !important;
    color: #ffffff !important;
    border: none !important;
    font-weight: 650 !important;
    box-shadow: none;
}
.stButton > button[kind="primary"]:hover {
    background: var(--color-primary-deep) !important;
    transform: translateY(-1px);
}
.stButton > button[kind="primary"]:active {
    transform: translateY(0) scale(0.985);
}
.stButton > button[kind="primary"]:focus-visible {
    outline: 2px solid var(--color-primary) !important;
    outline-offset: 2px !important;
}
.stButton > button[kind="secondary"] {
    background: var(--color-surface) !important;
    border: 1px solid var(--color-border) !important;
}
.stButton > button[kind="secondary"]:hover {
    border-color: var(--color-ink-muted) !important;
    color: var(--color-ink) !important;
    transform: translateY(-1px);
}
.stButton > button[kind="primary"] p { color: #ffffff !important; }

.stTextInput input, .stTextArea textarea, .stSelectbox div[data-baseweb="select"] > div {
    border-radius: var(--radius-sm) !important;
    border-color: var(--color-border) !important;
    background: var(--color-surface) !important;
}
.stTextInput input:focus, .stTextArea textarea:focus {
    border-color: var(--color-primary) !important;
    box-shadow: 0 0 0 2px rgba(217, 119, 6, 0.16) !important;
}

/* Barra de progresso Streamlit — só o trilho (sem texto sobreposto) */
div[data-testid="stProgress"] {
    margin: 0.35rem 0 0.85rem 0 !important;
}
div[data-testid="stProgress"] > div {
    background: var(--color-surface-muted) !important;
    border-radius: 999px !important;
    overflow: hidden !important;
    height: 0.5rem !important;
    min-height: 0.5rem !important;
}
div[data-testid="stProgress"] > div > div {
    background: linear-gradient(90deg, var(--color-primary-bright), var(--color-primary)) !important;
    border-radius: 999px !important;
    transition: width var(--dur-moderate) var(--ease-out-quart) !important;
    min-height: 0.5rem !important;
}
/* Esconde rótulo nativo se alguma versão do Streamlit ainda injetar texto na barra */
div[data-testid="stProgress"] p,
div[data-testid="stProgress"] [data-testid="stMarkdownContainer"],
div[data-testid="stProgress"] span[class*="progress"] {
    display: none !important;
}

div[data-testid="stAlert"] { border-radius: var(--radius-md) !important; }
label[data-testid="stWidgetLabel"] + div [role="checkbox"][aria-checked="true"] {
    background: var(--color-primary) !important;
    border-color: var(--color-primary-deep) !important;
}

@keyframes hero-entra {
    from { opacity: 0.86; transform: translateY(8px); }
    to { opacity: 1; transform: translateY(0); }
}
@keyframes nota-geral-entra {
    from { opacity: 0; transform: translateY(6px); }
    to { opacity: 1; transform: translateY(0); }
}
@keyframes hint-bounce {
    0%, 100% { transform: translateY(0); opacity: 1; }
    50% { transform: translateY(3px); opacity: 0.75; }
}
@keyframes resultado-entra {
    from { opacity: 0.9; transform: translateY(10px); }
    to { opacity: 1; transform: translateY(0); }
}
@keyframes painel-progresso-entra {
    from { opacity: 0.92; transform: translateY(4px); }
    to { opacity: 1; transform: translateY(0); }
}
@keyframes painel-aba-entra {
    from { opacity: 0.96; }
    to { opacity: 1; }
}
@keyframes etapa-ativa-pulso {
    0% { box-shadow: 0 0 0 0 rgba(217, 119, 6, 0.24); }
    100% { box-shadow: 0 0 0 8px rgba(217, 119, 6, 0); }
}
@keyframes pulso-indicador {
    0% { transform: scale(0.9); }
    100% { transform: scale(1); }
}

hr { border-color: var(--color-border) !important; opacity: 0.7; }
[data-testid="stStatusWidget"] { display: none !important; }

/* Mobile-First & Responsividade Industrial Avançada */
@media (max-width: 768px) {
    header[data-testid="stHeader"] {
        background: rgba(18, 16, 14, 0.95) !important;
        backdrop-filter: blur(12px) !important;
        border-bottom: 1px solid rgba(253, 186, 116, 0.2) !important;
    }
    header[data-testid="stHeader"] button {
        color: #fdba74 !important;
    }
    .main .block-container {
        padding-left: 0.85rem !important;
        padding-right: 0.85rem !important;
        padding-top: 0.5rem !important;
        padding-bottom: 2.5rem !important;
        max-width: 100vw !important;
        box-sizing: border-box !important;
    }
    .hero-bleed {
        margin-left: -0.85rem !important;
        margin-right: -0.85rem !important;
        width: calc(100% + 1.7rem) !important;
        left: 0 !important;
        right: 0 !important;
        border-radius: 0 0 var(--radius-lg) var(--radius-lg);
    }
    .hero-inner {
        padding: 1.75rem 0.85rem 2.25rem !important;
        display: flex !important;
        flex-direction: column !important;
        gap: 1.25rem !important;
    }
    .stApp .hero-bleed .hero-brand,
    .hero-bleed .hero-brand,
    .stApp h1.hero-brand {
        max-width: 100% !important;
        font-size: clamp(1.85rem, 8.5vw, 2.45rem) !important;
        line-height: 1.05 !important;
    }
    .hero-aside {
        border-left: none !important;
        border-top: 1px solid rgba(255, 255, 255, 0.12) !important;
        padding-left: 0 !important;
        padding-top: 0.85rem !important;
        flex-direction: row !important;
        justify-content: space-between !important;
        gap: 0.65rem !important;
    }
    .hero-stat-card {
        flex: 1 !important;
        padding: 0.55rem 0.65rem !important;
    }
    .hero-stat-card__val {
        font-size: 1.25rem !important;
    }
    .hero-quick-chips {
        gap: 0.4rem !important;
    }
    .hero-quick-chip {
        font-size: 0.72rem !important;
        padding: 0.25rem 0.55rem !important;
        color: #fffbeb !important;
    }
    /* Touch targets ergonômicos no mobile (chão de fábrica) */
    .stButton > button {
        min-height: 3.1rem !important;
        font-size: 0.96rem !important;
    }
    .fluxo-passos {
        grid-template-columns: repeat(3, 1fr) !important;
        gap: 0.35rem !important;
    }
    .fluxo-passo {
        padding: 0.5rem 0.35rem !important;
        font-size: 0.74rem !important;
        gap: 0.35rem !important;
    }
    .fluxo-passo__num {
        width: 1.25rem !important;
        height: 1.25rem !important;
        font-size: 0.68rem !important;
    }
    .kpi-command-deck {
        grid-template-columns: 1fr 1fr !important;
        gap: 0.55rem !important;
    }
    .plano-grid {
        grid-template-columns: 1fr !important;
        gap: 0.75rem !important;
    }
    .nota-geral {
        grid-template-columns: 1fr !important;
        gap: 0.35rem !important;
    }
}

@media (max-width: 480px) {
    .kpi-command-deck {
        grid-template-columns: 1fr !important;
    }
    .hero-aside {
        flex-direction: column !important;
    }
    .callout-24h__text {
        font-size: 0.95rem !important;
    }
}

@media (prefers-reduced-motion: reduce) {
    *, *::before, *::after {
        animation-duration: 0.01ms !important;
        animation-iteration-count: 1 !important;
        transition-duration: 0.01ms !important;
    }
    section[data-testid="stSidebar"] { transition: none !important; }
    .stButton > button:hover,
    .stButton > button:active {
        transform: none !important;
    }
}

/* Painel de status OpenCode Go na Sidebar */
.status-panel {
    display: flex;
    align-items: center;
    gap: 0.55rem;
    padding: 0.45rem 0.75rem;
    border-radius: var(--radius-md);
    font-size: 0.8rem;
    font-weight: 600;
    margin-bottom: 0.85rem;
    border: 1px solid transparent;
}
.badge-status-on {
    background: #ecfdf5;
    color: #047857;
    border-color: #a7f3d0;
}
.badge-status-off {
    background: #fef2f2;
    color: #991b1b;
    border-color: #fecaca;
}
.status-dot {
    width: 8px;
    height: 8px;
    border-radius: 50%;
    background-color: currentColor;
    display: inline-block;
    box-shadow: 0 0 6px currentColor;
    animation: pulse-dot 2s infinite ease-in-out;
}
@keyframes pulse-dot {
    0%, 100% { transform: scale(1); opacity: 1; }
    50% { transform: scale(1.25); opacity: 0.55; }
}

/* Badge no Hero */
.stApp .hero-bleed .hero-badge,
.hero-bleed .hero-badge,
.hero-badge {
    display: inline-flex !important;
    align-items: center !important;
    gap: 0.5rem !important;
    background: rgba(245, 158, 11, 0.14) !important;
    border: 1px solid rgba(253, 186, 116, 0.45) !important;
    padding: 0.35rem 0.95rem !important;
    border-radius: 9999px !important;
    font-size: 0.8rem !important;
    color: #fef08a !important; /* Dourado/âmbar claro */
    font-weight: 700 !important;
    letter-spacing: 0.03em !important;
    margin-bottom: 0.85rem !important;
    backdrop-filter: blur(8px) !important;
}
.stApp .hero-bleed .hero-badge span,
.hero-bleed .hero-badge span,
.hero-badge span {
    color: #fef08a !important;
}
.hero-badge__dot {
    width: 8px;
    height: 8px;
    border-radius: 50%;
    background-color: #f59e0b;
    box-shadow: 0 0 8px #f59e0b;
}

/* Cards dos Playbooks */
.playbook-mini-card {
    background: var(--color-surface);
    border: 1px solid var(--color-border);
    border-radius: var(--radius-md);
    padding: 0.75rem 0.85rem;
    margin-bottom: 0.45rem;
    transition: all var(--dur-fast) var(--ease-out);
    box-shadow: var(--shadow-sm);
}
.playbook-mini-card:hover {
    border-color: var(--color-primary-bright);
    box-shadow: 0 4px 14px rgba(217, 119, 6, 0.12);
    transform: translateY(-2px);
}
.playbook-mini-card--ativo {
    border-color: var(--color-primary);
    background: var(--color-primary-light);
}
.playbook-mini-card__tag {
    display: inline-block;
    font-size: 0.68rem;
    font-weight: 700;
    color: var(--color-primary-deep);
    letter-spacing: 0.05em;
    margin-bottom: 0.25rem;
}
.playbook-mini-card__title {
    font-size: 0.88rem !important;
    font-weight: 600 !important;
    color: var(--color-ink) !important;
    margin: 0 !important;
    line-height: 1.3 !important;
}

/* Hero Chips e Stat Cards */
.hero-quick-chips {
    display: flex;
    flex-wrap: wrap;
    gap: 0.6rem;
    margin-top: 1rem;
}
.stApp .hero-bleed .hero-quick-chip,
.hero-bleed .hero-quick-chip,
.hero-quick-chip {
    display: inline-flex !important;
    align-items: center !important;
    gap: 0.35rem !important;
    padding: 0.32rem 0.8rem !important;
    border-radius: 9999px !important;
    background: rgba(245, 158, 11, 0.16) !important;
    border: 1px solid rgba(253, 186, 116, 0.5) !important;
    color: #fffbeb !important; /* Branco marfim brilhante (nunca preto) */
    font-size: 0.8rem !important;
    font-weight: 700 !important;
    letter-spacing: 0.02em !important;
    backdrop-filter: blur(8px) !important;
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.3) !important;
    transition: all 0.2s ease !important;
}
.stApp .hero-bleed .hero-quick-chip:hover,
.hero-bleed .hero-quick-chip:hover,
.hero-quick-chip:hover {
    background: rgba(245, 158, 11, 0.3) !important;
    border-color: #f59e0b !important;
    color: #ffffff !important;
    transform: translateY(-2px) !important;
    box-shadow: 0 4px 14px rgba(217, 119, 6, 0.35) !important;
}
.stApp .hero-bleed .hero-stat-card,
.hero-bleed .hero-stat-card,
.hero-stat-card {
    background: rgba(255, 255, 255, 0.07) !important;
    border: 1px solid rgba(253, 186, 116, 0.3) !important;
    border-radius: var(--radius-md) !important;
    padding: 0.75rem 1rem !important;
    backdrop-filter: blur(10px) !important;
}
.stApp .hero-bleed .hero-stat-card__val,
.hero-bleed .hero-stat-card__val,
.hero-stat-card__val {
    display: block !important;
    font-family: var(--font-display) !important;
    font-size: 1.5rem !important;
    font-weight: 800 !important;
    color: #fdba74 !important; /* Cobre luminoso */
    line-height: 1 !important;
}
.stApp .hero-bleed .hero-stat-card__desc,
.hero-bleed .hero-stat-card__desc,
.hero-stat-card__desc {
    display: block !important;
    font-size: 0.78rem !important;
    color: #e7e5e4 !important; /* Branco claro */
    margin-top: 0.3rem !important;
    font-weight: 500 !important;
}

/* Dossiê Executivo de Resultados */
.executive-dossier-header {
    display: flex;
    justify-content: space-between;
    align-items: flex-start;
    border-bottom: 1px solid var(--color-border);
    padding-bottom: 0.85rem;
    margin-bottom: 1.25rem;
}
.executive-dossier-tag {
    font-size: 0.7rem;
    font-weight: 750;
    letter-spacing: 0.12em;
    color: var(--color-primary-deep);
    text-transform: uppercase;
}
.executive-dossier-title {
    font-family: var(--font-display) !important;
    font-size: 1.6rem !important;
    font-weight: 700 !important;
    color: var(--color-ink) !important;
    margin: 0.2rem 0 0 0 !important;
    letter-spacing: -0.02em;
}
.executive-dossier-badge {
    display: inline-flex;
    align-items: center;
    padding: 0.25rem 0.65rem;
    border-radius: var(--radius-sm);
    background: #ecfdf5;
    color: #047857;
    border: 1px solid #a7f3d0;
    font-size: 0.72rem;
    font-weight: 700;
    letter-spacing: 0.05em;
}

/* KPI Command Deck */
.kpi-command-deck {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
    gap: 0.75rem;
    margin-bottom: 1.25rem;
}
.kpi-stat-chip {
    background: var(--color-surface-subtle);
    border: 1px solid var(--color-border);
    border-radius: var(--radius-md);
    padding: 0.65rem 0.85rem;
    display: flex;
    flex-direction: column;
    gap: 0.25rem;
}
.kpi-stat-chip__label {
    font-size: 0.65rem;
    font-weight: 700;
    letter-spacing: 0.08em;
    color: var(--color-ink-caption);
    text-transform: uppercase;
}
.kpi-stat-chip__value {
    font-family: var(--font-display);
    font-size: 0.98rem;
    font-weight: 650;
    color: var(--color-ink);
}
.kpi-stat-chip__value--subtle {
    font-size: 0.82rem;
    color: var(--color-ink-muted);
}
.kpi-stat-chip__value--accent {
    font-size: 0.85rem;
    color: var(--color-primary-deep);
    font-weight: 700;
}
.kpi-stat-chip__pill {
    display: inline-block;
    padding: 0.15rem 0.5rem;
    border-radius: var(--radius-sm);
    font-size: 0.78rem;
    font-weight: 700;
    width: fit-content;
}
.pill-alta { background: #fef2f2; color: #991b1b; border: 1px solid #fecaca; }
.pill-media { background: #fffbeb; color: #92400e; border: 1px solid #fde68a; }
.pill-baixa { background: #ecfdf5; color: #047857; border: 1px solid #a7f3d0; }

/* Callout Prioridade 24 Horas */
.callout-24h {
    display: flex;
    background: linear-gradient(135deg, #fffbeb 0%, #fff7ed 100%);
    border: 1px solid #fde68a;
    border-left: 5px solid var(--color-primary);
    border-radius: var(--radius-md);
    margin-bottom: 1.5rem;
    box-shadow: 0 4px 16px rgba(217, 119, 6, 0.08);
    overflow: hidden;
}
.callout-24h__content {
    padding: 1rem 1.25rem;
    width: 100%;
}
.callout-24h__header {
    display: flex;
    align-items: center;
    gap: 0.45rem;
    margin-bottom: 0.45rem;
}
.callout-24h__icon {
    font-size: 1.1rem;
}
.callout-24h__title {
    font-size: 0.78rem;
    font-weight: 800;
    letter-spacing: 0.08em;
    color: var(--color-primary-deep);
}
.callout-24h__text {
    font-size: 1.05rem !important;
    font-weight: 600 !important;
    color: #451a03 !important;
    line-height: 1.45 !important;
    margin: 0 !important;
}

/* Destaques e Bullets */
.destaque-resumo {
    background: var(--color-surface);
    border: 1px solid var(--color-border);
    border-radius: var(--radius-md);
    padding: 1rem 1.15rem;
    font-size: 0.95rem;
    line-height: 1.55;
    color: var(--color-ink-body);
    margin-bottom: 1rem;
}
.destaque-bullet {
    display: flex;
    align-items: flex-start;
    gap: 0.5rem;
    margin-bottom: 0.5rem;
    font-size: 0.92rem;
    color: var(--color-ink-body);
}
.destaque-bullet__icon {
    color: var(--color-primary);
    font-weight: 700;
}

/* Plano Tático Grid */
.plano-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
    gap: 1rem;
    margin-top: 0.85rem;
}
.plano-passo-card {
    background: var(--color-surface);
    border: 1px solid var(--color-border);
    border-radius: var(--radius-md);
    padding: 1rem;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
    transition: all var(--dur-fast) var(--ease-out);
    box-shadow: var(--shadow-sm);
}
.plano-passo-card:hover {
    border-color: var(--color-primary-bright);
    transform: translateY(-2px);
    box-shadow: 0 6px 18px rgba(0,0,0,0.06);
}
.plano-passo-card__header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 0.65rem;
}
.plano-passo-card__badge {
    font-size: 0.65rem;
    font-weight: 800;
    padding: 0.15rem 0.45rem;
    border-radius: var(--radius-sm);
    background: var(--color-primary-light);
    color: var(--color-primary-deep);
    border: 1px solid var(--color-primary-border);
}
.plano-passo-card__prazo {
    font-size: 0.75rem;
    font-weight: 600;
    color: var(--color-ink-muted);
}
.plano-passo-card__titulo {
    font-family: var(--font-display) !important;
    font-size: 1.02rem !important;
    font-weight: 700 !important;
    color: var(--color-ink) !important;
    margin: 0 0 0.4rem 0 !important;
}
.plano-passo-card__acao {
    font-size: 0.88rem !important;
    color: var(--color-ink-body) !important;
    line-height: 1.45 !important;
    margin-bottom: 0.75rem !important;
}
.plano-passo-card__footer {
    border-top: 1px solid var(--color-surface-muted);
    padding-top: 0.5rem;
}
.plano-passo-card__resp {
    font-size: 0.75rem;
    color: var(--color-ink-muted);
}

/* Roteiro SBI */
.sbi-intro-box {
    background: var(--color-surface-subtle);
    border: 1px solid var(--color-border);
    border-radius: var(--radius-md);
    padding: 0.85rem 1.15rem;
    margin-bottom: 1rem;
}
.sbi-intro-box__tag {
    font-size: 0.65rem;
    font-weight: 800;
    letter-spacing: 0.08em;
    color: var(--color-primary-deep);
}
.sbi-intro-box__title {
    font-family: var(--font-display) !important;
    font-size: 1.05rem !important;
    font-weight: 700 !important;
    color: var(--color-ink) !important;
    margin: 0.2rem 0 !important;
}
.sbi-intro-box__desc {
    font-size: 0.85rem !important;
    color: var(--color-ink-muted) !important;
    margin: 0 !important;
}
.sbi-dialog-card {
    background: var(--color-surface);
    border-left: 3px solid var(--color-primary);
    border-top: 1px solid var(--color-border);
    border-right: 1px solid var(--color-border);
    border-bottom: 1px solid var(--color-border);
    border-radius: var(--radius-sm);
    padding: 0.75rem 1rem;
    margin-bottom: 0.65rem;
}
.sbi-dialog-card__text {
    font-size: 0.92rem !important;
    line-height: 1.55 !important;
    color: var(--color-ink) !important;
    margin: 0 !important;
}

/* Estilização Moderna de Abas do Streamlit */
div[data-baseweb="tab-list"] {
    gap: 0.4rem !important;
    border-bottom: 1px solid var(--color-border) !important;
    padding-bottom: 0.25rem !important;
    margin-bottom: 1rem !important;
}
button[data-baseweb="tab"] {
    font-family: var(--font-display) !important;
    font-size: 0.9rem !important;
    font-weight: 600 !important;
    padding: 0.45rem 0.95rem !important;
    border-radius: var(--radius-md) var(--radius-md) 0 0 !important;
    color: var(--color-ink-muted) !important;
    transition: all var(--dur-fast) var(--ease-out) !important;
}
button[data-baseweb="tab"]:hover {
    color: var(--color-ink) !important;
    background: var(--color-surface-subtle) !important;
}
button[data-baseweb="tab"][aria-selected="true"] {
    color: var(--color-primary-deep) !important;
    background: var(--color-surface) !important;
    border-bottom: 2px solid var(--color-primary) !important;
    font-weight: 700 !important;
}

/* =========================================================================
   AGENT TELEMETRY RADAR (HUD DE ANÁLISE EM TEMPO REAL)
   ========================================================================= */
.agent-telemetry-hud {
    background: linear-gradient(135deg, #100e0d 0%, #1c1917 55%, #292524 100%);
    border: 1px solid rgba(245, 158, 11, 0.4);
    border-radius: var(--radius-lg);
    padding: 1.35rem 1.5rem;
    margin: 1rem 0 1.25rem;
    box-shadow: 0 12px 36px rgba(0, 0, 0, 0.35), 0 0 20px rgba(217, 119, 6, 0.18);
    position: relative;
    overflow: hidden;
    color: #ffffff;
    animation: painel-progresso-entra var(--dur-normal) var(--ease-out-quart) both;
}
.agent-telemetry-hud::before {
    content: "";
    position: absolute;
    top: 0;
    left: -100%;
    width: 100%;
    height: 3px;
    background: linear-gradient(90deg, transparent, #f59e0b, #fdba74, transparent);
    animation: radar-sweep 2s linear infinite;
}
@keyframes radar-sweep {
    0% { left: -100%; }
    100% { left: 100%; }
}
.agent-telemetry-top {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 0.85rem;
    flex-wrap: wrap;
    gap: 0.5rem;
}
.agent-radar-title-group {
    display: flex;
    align-items: center;
    gap: 0.65rem;
}
.agent-radar-pulse {
    position: relative;
    width: 11px;
    height: 11px;
    background: #10b981;
    border-radius: 50%;
    box-shadow: 0 0 8px #10b981;
}
.agent-radar-pulse::after {
    content: "";
    position: absolute;
    inset: -4px;
    border-radius: 50%;
    border: 2px solid #10b981;
    animation: radar-ring 1.8s ease-out infinite;
}
@keyframes radar-ring {
    0% { transform: scale(0.8); opacity: 1; }
    100% { transform: scale(2.2); opacity: 0; }
}
.agent-radar-title {
    font-family: var(--font-display) !important;
    font-size: 1.05rem !important;
    font-weight: 700 !important;
    color: #ffffff !important;
    letter-spacing: -0.01em;
    margin: 0 !important;
}
.agent-radar-engine-tag {
    display: inline-flex;
    align-items: center;
    gap: 0.4rem;
    background: rgba(255, 255, 255, 0.08);
    border: 1px solid rgba(253, 186, 116, 0.35);
    padding: 0.22rem 0.65rem;
    border-radius: 9999px;
    font-size: 0.72rem;
    font-weight: 600;
    color: #fde68a;
    backdrop-filter: blur(4px);
}
.agent-telemetry-step {
    font-size: 0.96rem;
    color: #e7e5e4;
    margin-bottom: 0.65rem;
    font-weight: 550;
    display: flex;
    align-items: center;
    gap: 0.5rem;
}
.agent-telemetry-step__badge {
    background: rgba(217, 119, 6, 0.25);
    border: 1px solid #d97706;
    color: #fdba74;
    padding: 0.15rem 0.45rem;
    border-radius: var(--radius-sm);
    font-size: 0.72rem;
    font-weight: 700;
}
.agent-telemetry-metrics {
    display: flex;
    justify-content: space-between;
    font-size: 0.76rem;
    color: #fdba74;
    font-weight: 600;
    margin-top: 0.55rem;
}

/* =========================================================================
   GRAVADOR DE ÁUDIO NO CHÃO DE FÁBRICA (MOBILE & FACTORY FLOOR)
   ========================================================================= */
.audio-recorder-box {
    background: linear-gradient(135deg, #1c1917 0%, #292524 100%);
    border: 1px dashed rgba(245, 158, 11, 0.45);
    border-radius: var(--radius-md);
    padding: 0.85rem 1rem;
    margin-bottom: 0.85rem;
    color: #ffffff;
}
.audio-recorder-box__header {
    display: flex;
    align-items: center;
    gap: 0.5rem;
    margin-bottom: 0.35rem;
}
.audio-recorder-box__icon {
    font-size: 1.1rem;
}
.audio-recorder-box__title {
    font-size: 0.8rem;
    font-weight: 750;
    letter-spacing: 0.08em;
    text-transform: uppercase;
    color: #fdba74;
    margin: 0;
}
.audio-recorder-box__desc {
    font-size: 0.78rem;
    color: #d6d3d1;
    margin-bottom: 0.55rem;
    line-height: 1.4;
}

/* =========================================================================
   CHECKLIST INTERATIVO DE AÇÕES NO CHÃO DE FÁBRICA
   ========================================================================= */
.checklist-plano-item {
    background: var(--color-surface);
    border: 1px solid var(--color-border);
    border-radius: var(--radius-sm);
    padding: 0.55rem 0.85rem;
    margin-bottom: 0.45rem;
    display: flex;
    align-items: center;
    gap: 0.65rem;
    transition: all var(--dur-fast) var(--ease-out);
}
.checklist-plano-item:hover {
    border-color: var(--color-primary-bright);
    background: var(--color-surface-subtle);
}
.checklist-plano-item--concluido {
    background: var(--color-complete-bg);
    border-color: var(--color-complete-border);
    text-decoration: line-through;
    opacity: 0.75;
}
</style>
"""

JS_PT_BR = """
<script>
(function () {
  const mapa = {
    "File change.": "Arquivo alterado.",
    "Source file changed.": "Arquivo-fonte alterado.",
    "Rerun": "Executar novamente",
    "Always rerun": "Sempre executar novamente",
    "Running...": "Executando...",
    "Running": "Executando",
    "Deploy": "Publicar",
    "Clear cache": "Limpar cache",
    "About": "Sobre",
    "Settings": "Configurações",
    "Print": "Imprimir",
    "Record a screencast": "Gravar tela",
    "Choose an option": "Selecione uma opção",
    "No results": "Nenhum resultado",
    "Press Enter to apply": "Pressione Enter para aplicar",
    "Press Enter to submit form": "Pressione Enter para enviar",
    "Connection error": "Erro de conexão",
    "Connection lost": "Conexão perdida",
    "Reconnecting...": "Reconectando...",
  };

  function traduzirNo(no) {
    if (!no || no.nodeType !== Node.TEXT_NODE) return;
    const original = no.textContent;
    const chave = original.trim();
    if (mapa[chave]) no.textContent = original.replace(chave, mapa[chave]);
  }

  function traduzirArvore(raiz) {
    if (!raiz) return;
    const walker = document.createTreeWalker(raiz, NodeFilter.SHOW_TEXT);
    let no;
    while ((no = walker.nextNode())) traduzirNo(no);
  }

  document.documentElement.lang = "pt-BR";
  traduzirArvore(document.body);

  const obs = new MutationObserver((muts) => {
    for (const m of muts) {
      if (m.type === "childList") {
        m.addedNodes.forEach((n) => {
          if (n.nodeType === Node.TEXT_NODE) traduzirNo(n);
          else if (n.nodeType === Node.ELEMENT_NODE) traduzirArvore(n);
        });
      } else if (m.type === "characterData") traduzirNo(m.target);
    }
  });
  obs.observe(document.body, { childList: true, subtree: true, characterData: true });
})();
</script>
"""


def injetar_estilos():
    """Injeta CSS do tema moderno e script de localização PT-BR."""
    import streamlit as st

    st.markdown(CSS_APP, unsafe_allow_html=True)
    if hasattr(st, "html"):
        st.html(JS_PT_BR)
    else:
        import streamlit.components.v1 as components

        components.html(JS_PT_BR, height=0, width=0)


_COR_TIPO = {
    "lideranca": "#57534e",
    "comunicacao": "#78716c",
    "conflito": "#b45309",
    "desempenho": "#d97706",
    "processo": "#57534e",
    "seguranca": "#9a3412",
}


def cor_tipo_problema(tipo: str) -> str:
    return _COR_TIPO.get((tipo or "").lower(), "#a8a29e")


def classe_tipo_problema(tipo: str) -> str:
    """Mantido por compatibilidade; acento via cor_tipo_problema + CSS var."""
    mapa = {
        "lideranca": "tipo-lideranca",
        "comunicacao": "tipo-comunicacao",
        "conflito": "tipo-conflito",
        "desempenho": "tipo-desempenho",
        "processo": "tipo-processo",
        "seguranca": "tipo-seguranca",
    }
    return mapa.get((tipo or "").lower(), "tipo-default")
