"""Estilos CSS — tema claro alinhado a DESIGN.md."""

CSS_APP = """
<style>
:root {
    /* Marca — cobre industrial (família laranja) */
    --color-primary: #e67e22;
    --color-primary-bright: #eb8f3a;
    --color-primary-deep: #b45309;
    --color-primary-light: #f8f3ed;
    --color-primary-border: #e5d0b8;

    /* Hero — bronze profundo (par com o laranja, sem azul) */
    --color-hero-from: #4a2f1a;
    --color-hero-to: #7a4520;
    --color-hero-muted: #fff3e8;
    --color-hero-subtitle: #f5e6d8;

    /* Neutros com leve tinte quente */
    --color-ink: #1c1917;
    --color-ink-secondary: #292524;
    --color-ink-body: #44403c;
    --color-ink-muted: #6b6560;
    --color-ink-caption: #9c958e;
    --color-surface: #ffffff;
    --color-surface-subtle: #faf8f5;
    --color-surface-muted: #f3efe9;
    --color-border: #e8dfd4;

    /* Completude — cobre suave */
    --color-complete-bg: #faefe3;
    --color-complete-ink: #7a4520;
    --color-complete-border: #e5c49a;
    --color-success-bg: var(--color-complete-bg);
    --color-success-ink: var(--color-complete-ink);
    --color-success-border: var(--color-complete-border);

    /* Aviso e ativo — família cobre */
    --color-warning-bg: #faf3eb;
    --color-warning-ink: #92400e;
    --color-warning-border: var(--color-primary-border);
    --color-active-bg: #fdf4ea;
    --color-active-ink: #9a3412;
    --color-active-border: var(--color-primary-border);

    /* Confirmação de resultado — cobre quente (par com o laranja) */
    --color-confirm-bg: #faefe3;
    --color-confirm-ink: #9a4a18;
    --color-confirm-border: #e5c49a;

    /* Erro e info alinhados à paleta */
    --color-error-bg: #faf0ee;
    --color-error-ink: #8b3a32;
    --color-error-border: #e5c4be;
    --color-info-bg: #faefe3;
    --color-info-ink: #7a4520;
    --color-info-border: var(--color-complete-border);

    /* Tipos — escala cobre (sem azul) */
    --color-tipo-lideranca: #6b4423;
    --color-tipo-comunicacao: #7a4e28;
    --color-tipo-conflito: #a84832;
    --color-tipo-desempenho: #c76a2a;
    --color-tipo-processo: #8b5a32;
    --color-tipo-seguranca: #8b3a32;
    --color-tipo-default: var(--color-ink-caption);

    --radius-sm: 8px;
    --radius-md: 10px;
    --radius-lg: 12px;
    --radius-xl: 16px;
    --space-xs: 0.45rem;
    --space-sm: 0.85rem;
    --space-md: 1.25rem;
    --space-lg: 1.5rem;
    --space-xl: 2rem;
    --shadow-sm: 0 1px 6px rgba(74, 47, 26, 0.08);
    --shadow-md: 0 8px 28px rgba(74, 47, 26, 0.14);
    --ease-out: cubic-bezier(0.22, 1, 0.36, 1);
    --ease-out-quart: cubic-bezier(0.25, 1, 0.5, 1);
    --ease-out-expo: cubic-bezier(0.16, 1, 0.3, 1);
    --dur-instant: 120ms;
    --dur-fast: 180ms;
    --dur-normal: 220ms;
    --dur-moderate: 280ms;
}

html, body, [class*="css"] {
    font-family: system-ui, -apple-system, 'Segoe UI', sans-serif;
    -webkit-font-smoothing: antialiased;
}

.stApp {
    background: linear-gradient(180deg, var(--color-surface-subtle) 0%, var(--color-surface-muted) 100%) !important;
    color: var(--color-ink);
    line-height: 1.55;
}

header[data-testid="stHeader"] {
    background: var(--color-surface) !important;
    border-bottom: 1px solid var(--color-border) !important;
}
div[data-testid="stDecoration"] {
    background: var(--color-surface) !important;
    background-image: none !important;
}

.main .block-container {
    padding-top: var(--space-md) !important;
    padding-bottom: var(--space-xl) !important;
    max-width: 1000px;
}

.stApp h1, .stApp h2, .stApp h3 { color: var(--color-ink) !important; }
.stApp h4, .stApp h5, .stApp h6 { color: var(--color-ink-secondary) !important; }
.stApp p, .stApp li { color: var(--color-ink-body) !important; max-width: 72ch; }
.stApp label { color: var(--color-ink-muted) !important; font-weight: 500 !important; }
.stApp .stCaption { color: var(--color-ink-muted) !important; }

/* Hero — compacto, família cobre */
.hero-container {
    background: linear-gradient(160deg, var(--color-hero-from) 0%, var(--color-hero-to) 100%);
    border-radius: var(--radius-lg);
    padding: 1.35rem 1.75rem;
    margin-bottom: var(--space-lg);
    box-shadow: var(--shadow-md);
    border: 1px solid rgba(255, 255, 255, 0.12);
}
.hero-container .hero-eyebrow {
    color: var(--color-hero-muted) !important;
    font-size: 0.72rem !important;
    font-weight: 600 !important;
    letter-spacing: 0.06em !important;
    text-transform: uppercase !important;
    margin: 0 0 0.35rem 0 !important;
    max-width: none !important;
    opacity: 1 !important;
}
.hero-container .hero-title {
    color: #ffffff !important;
    font-size: clamp(1.35rem, 2.5vw, 1.75rem) !important;
    font-weight: 700 !important;
    margin: 0 0 0.4rem 0 !important;
    max-width: none !important;
    text-wrap: balance;
}
.hero-container .hero-subtitle {
    color: var(--color-hero-subtitle) !important;
    font-size: 0.95rem !important;
    line-height: 1.55 !important;
    margin: 0 !important;
    max-width: 58ch !important;
}

/* Fluxo — passos do wizard */
.fluxo-passos {
    display: flex;
    gap: 0.5rem;
    margin-bottom: var(--space-md);
    flex-wrap: wrap;
}
.fluxo-passo {
    display: flex;
    align-items: center;
    gap: 0.5rem;
    flex: 1;
    min-width: 140px;
    padding: 0.55rem 0.75rem;
    border-radius: var(--radius-sm);
    border: 1px solid var(--color-border);
    background: var(--color-surface-muted);
    font-size: 0.82rem;
    color: var(--color-ink-muted);
    transition:
        background var(--dur-fast) var(--ease-out-quart),
        border-color var(--dur-fast) var(--ease-out-quart),
        color var(--dur-fast) var(--ease-out-quart),
        box-shadow var(--dur-fast) var(--ease-out-quart);
}
.fluxo-passo--active {
    background: var(--color-surface);
    border-color: var(--color-primary);
    color: var(--color-ink);
    box-shadow: var(--shadow-sm);
}
.fluxo-passo--done {
    background: var(--color-complete-bg);
    border-color: var(--color-complete-border);
    color: var(--color-complete-ink);
}
.fluxo-passo--pending { opacity: 0.72; }
.fluxo-passo__num {
    display: inline-flex;
    align-items: center;
    justify-content: center;
    width: 1.35rem;
    height: 1.35rem;
    border-radius: 999px;
    font-size: 0.72rem;
    font-weight: 700;
    background: var(--color-border);
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
.fluxo-passo__label { font-weight: 500; line-height: 1.3; }

/* Wizard panel */
.wizard-panel-marker { display: none; }
.wizard-panel-marker + div[data-testid="stVerticalBlockBorderWrapper"] {
    background: var(--color-surface) !important;
    border-color: var(--color-border) !important;
    border-radius: var(--radius-lg) !important;
    padding: var(--space-md) var(--space-lg) !important;
    margin-bottom: var(--space-md) !important;
    box-shadow: var(--shadow-sm) !important;
}
.wizard-panel {
    background: var(--color-surface);
    border: 1px solid var(--color-border);
    border-radius: var(--radius-lg);
    padding: var(--space-lg);
    margin-bottom: var(--space-md);
    box-shadow: var(--shadow-sm);
}
.wizard-secao-titulo {
    color: var(--color-ink) !important;
    font-size: 1rem !important;
    font-weight: 600 !important;
    margin: 0 0 0.85rem 0 !important;
    padding: 0 !important;
    border: none !important;
}
.wizard-tipo-desc {
    background: var(--color-surface-subtle);
    border: 1px solid var(--color-border);
    border-radius: var(--radius-sm);
    padding: 0.65rem 0.85rem;
    font-size: 0.88rem;
    color: var(--color-ink-body);
    margin: 0.25rem 0 1rem;
}
.wizard-hint {
    background: var(--color-surface);
    border: 1px dashed var(--color-border);
    border-radius: var(--radius-lg);
    padding: var(--space-md);
    color: var(--color-ink-muted);
    font-size: 0.92rem;
    margin: 0.5rem 0 1rem;
}

/* Cards de métrica — acento no topo, sem faixa lateral */
.metric-card {
    background: var(--color-surface);
    border: 1px solid var(--color-border);
    border-top: 3px solid var(--metric-accent, var(--color-ink-caption));
    border-radius: var(--radius-lg);
    padding: var(--space-md) 1.25rem;
    text-align: center;
    box-shadow: var(--shadow-sm);
    min-height: 5.5rem;
    display: flex;
    flex-direction: column;
    justify-content: center;
    transition: box-shadow var(--dur-fast) var(--ease-out-quart), transform var(--dur-fast) var(--ease-out-quart);
}
.metric-card:hover {
    transform: translateY(-2px);
    box-shadow: 0 4px 14px rgba(15, 45, 74, 0.1);
}
.metric-card h4 {
    color: var(--color-ink-muted);
    font-size: 0.78rem;
    font-weight: 500;
    text-transform: uppercase;
    letter-spacing: 0.04em;
    margin: 0;
}
.metric-card p {
    color: var(--color-ink) !important;
    font-size: 1.2rem;
    font-weight: 700;
    margin: 0.35rem 0 0 0;
    max-width: none !important;
}

.resultado-banner {
    background: var(--color-confirm-bg);
    border: 1px solid var(--color-confirm-border);
    color: var(--color-confirm-ink);
    border-radius: var(--radius-lg);
    padding: 0.85rem 1.1rem;
    font-weight: 600;
    margin-bottom: var(--space-md);
    animation: banner-confirmacao var(--dur-normal) var(--ease-out-quart) both;
}

/* Shell editorial dos resultados */
.resultado-shell-marker { display: none; }
.resultado-shell-marker + div[data-testid="stVerticalBlockBorderWrapper"] {
    background: var(--color-surface) !important;
    border-color: var(--color-border) !important;
    border-radius: var(--radius-lg) !important;
    padding: var(--space-lg) !important;
    margin-top: var(--space-md) !important;
    margin-bottom: var(--space-md) !important;
    box-shadow: var(--shadow-sm) !important;
}
.resultado-shell {
    background: var(--color-surface);
    border: 1px solid var(--color-border);
    border-radius: var(--radius-lg);
    padding: var(--space-lg);
    margin-top: var(--space-md);
    box-shadow: var(--shadow-sm);
}
.resultado-shell__header {
    display: flex;
    flex-wrap: wrap;
    align-items: baseline;
    justify-content: space-between;
    gap: 0.5rem;
    margin-bottom: var(--space-md);
    padding-bottom: var(--space-sm);
    border-bottom: 1px solid var(--color-border);
}
.resultado-shell__titulo {
    color: var(--color-ink) !important;
    font-size: 1.15rem !important;
    font-weight: 700 !important;
    margin: 0 !important;
}
.resultado-shell__meta {
    font-size: 0.8rem;
    color: var(--color-ink-caption);
}

/* Painel de progresso (área principal) */
.progresso-painel {
    background: var(--color-surface);
    border: 1px solid var(--color-border);
    border-radius: var(--radius-lg);
    padding: var(--space-lg);
    margin: var(--space-md) 0;
    box-shadow: var(--shadow-sm);
    animation: painel-progresso-entra var(--dur-normal) var(--ease-out-quart) both;
}
.progresso-painel__titulo {
    color: var(--color-ink) !important;
    font-size: 1rem !important;
    font-weight: 600 !important;
    margin: 0 0 0.35rem 0 !important;
}
.progresso-painel__etapa {
    color: var(--color-ink-body) !important;
    font-size: 0.92rem !important;
    margin: 0 0 0.25rem 0 !important;
}
.progresso-painel__pct {
    color: var(--color-ink-caption) !important;
    font-size: 0.78rem !important;
    margin: 0 0 0.75rem 0 !important;
}

/* Timeline horizontal */
.timeline-horizontal {
    display: flex;
    gap: 0.35rem;
    margin-top: var(--space-sm);
    flex-wrap: wrap;
}
.timeline-h-item {
    flex: 1;
    min-width: 72px;
    text-align: center;
    padding: 0.45rem 0.35rem;
    border-radius: var(--radius-sm);
    font-size: 0.72rem;
    border: 1px solid transparent;
    transition:
        background var(--dur-fast) var(--ease-out-quart),
        border-color var(--dur-fast) var(--ease-out-quart),
        color var(--dur-fast) var(--ease-out-quart);
}
.timeline-h-icon { display: block; font-size: 0.85rem; margin-bottom: 0.15rem; transition: transform var(--dur-fast) var(--ease-out-quart); }
.timeline-h-label { display: block; line-height: 1.25; }
.timeline-h-item.timeline-active {
    animation: etapa-ativa-pulso 0.42s var(--ease-out-expo);
}
.timeline-h-item.timeline-done .timeline-h-icon {
    transform: scale(1.08);
}

/* Alertas */
.alerta {
    border-radius: var(--radius-sm);
    padding: 0.75rem 0.9rem;
    font-size: 0.88rem;
    line-height: 1.45;
    margin: 0.5rem 0;
    animation: painel-progresso-entra var(--dur-normal) var(--ease-out-quart) both;
}
.alerta--erro { background: var(--color-error-bg); border: 1px solid var(--color-error-border); color: var(--color-error-ink); }
.alerta--aviso { background: var(--color-warning-bg); border: 1px solid var(--color-warning-border); color: var(--color-warning-ink); }
.alerta--info { background: var(--color-info-bg); border: 1px solid var(--color-info-border); color: var(--color-info-ink); }

.proximo-passo-card {
    background: var(--color-primary-light);
    border: 1px solid var(--color-primary-border);
    border-radius: var(--radius-lg);
    padding: 1.1rem 1.25rem;
    margin: var(--space-md) 0;
    color: var(--color-ink-secondary);
    line-height: 1.55;
    box-shadow: var(--shadow-sm);
    transition: box-shadow var(--dur-fast) var(--ease-out-quart), border-color var(--dur-fast) var(--ease-out-quart);
}
.proximo-passo-card:hover {
    box-shadow: 0 2px 10px rgba(230, 126, 34, 0.12);
}
.proximo-passo-card strong {
    display: block;
    color: var(--color-primary-deep);
    font-size: 0.78rem;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.04em;
    margin-bottom: 0.5rem;
}
.proximo-passo-card p {
    margin: 0 !important;
    color: var(--color-ink-secondary) !important;
    font-size: 0.98rem !important;
    max-width: none !important;
}

.section-heading {
    color: var(--color-ink) !important;
    font-size: 1.05rem !important;
    font-weight: 600 !important;
    margin: 0 0 0.75rem 0 !important;
    padding-bottom: 0.35rem;
    border-bottom: 1px solid var(--color-border);
}

.timeline-step {
    padding: var(--space-xs) var(--space-sm);
    border-radius: var(--radius-sm);
    margin: 0.2rem 0;
    font-size: 0.85rem;
    border: 1px solid transparent;
    transition:
        background var(--dur-fast) var(--ease-out-quart),
        border-color var(--dur-fast) var(--ease-out-quart),
        color var(--dur-fast) var(--ease-out-quart);
}
.timeline-done { background: var(--color-complete-bg); color: var(--color-complete-ink); border-color: var(--color-complete-border); }
.timeline-active {
    background: var(--color-active-bg);
    color: var(--color-active-ink);
    font-weight: 600;
    border-color: var(--color-active-border);
    animation: etapa-ativa-pulso 0.42s var(--ease-out-expo);
}
.timeline-pending { background: var(--color-surface-muted); color: var(--color-ink-caption); }

.aviso-publico {
    background: var(--color-warning-bg);
    color: var(--color-warning-ink);
    border: 1px solid var(--color-warning-border);
    padding: 0.7rem 0.9rem;
    border-radius: var(--radius-sm);
    font-size: 0.82rem;
    line-height: 1.45;
}

.rodape-app {
    width: 100%;
    margin-top: var(--space-xl);
    text-align: center;
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
    box-sizing: border-box;
}

/* Sidebar */
section[data-testid="stSidebar"] {
    position: fixed !important;
    left: 0 !important;
    top: 3.5rem !important;
    height: calc(100vh - 3.5rem) !important;
    z-index: 999900 !important;
    transform: translateX(calc(-100% + 14px)) !important;
    transition: transform 0.22s var(--ease-out) !important;
    box-shadow: 2px 0 16px rgba(15, 23, 42, 0.08) !important;
    border-right: 1px solid var(--color-border) !important;
    overflow-y: auto !important;
}
section[data-testid="stSidebar"]:hover { transform: translateX(0) !important; }
section[data-testid="stSidebar"]::after {
    content: "›";
    position: fixed;
    left: 4px;
    top: 50%;
    color: var(--color-primary);
    font-size: 1.2rem;
    font-weight: 700;
    pointer-events: none;
    opacity: 0.9;
    z-index: 999901;
}
section[data-testid="stSidebar"]:hover::after { opacity: 0; }

section[data-testid="stSidebar"],
section[data-testid="stSidebar"] > div,
div[data-testid="stSidebarContent"] {
    background: var(--color-surface) !important;
}
section[data-testid="stMain"] { margin-left: 0 !important; }

/* Tabs */
.stTabs [data-baseweb="tab-list"] {
    border-bottom: 2px solid var(--color-border);
    gap: 0.25rem;
}
.stTabs [data-baseweb="tab"] {
    color: var(--color-ink-muted) !important;
    font-weight: 500 !important;
    padding: 0.55rem 0.9rem !important;
    transition: color var(--dur-fast) var(--ease-out-quart), border-color var(--dur-fast) var(--ease-out-quart) !important;
}
.stTabs [aria-selected="true"] {
    color: var(--color-ink) !important;
    border-bottom: 2px solid var(--color-primary) !important;
    background: transparent !important;
    font-weight: 600 !important;
}
.stTabs [data-baseweb="tab-panel"] {
    padding-top: var(--space-md) !important;
    animation: painel-aba-entra var(--dur-normal) var(--ease-out-quart) both;
}

div[data-testid="stExpander"] {
    background: var(--color-surface) !important;
    border: 1px solid var(--color-border) !important;
    border-radius: var(--radius-md);
    transition: border-color var(--dur-fast) var(--ease-out-quart), box-shadow var(--dur-fast) var(--ease-out-quart) !important;
}
div[data-testid="stExpander"]:focus-within {
    border-color: var(--color-primary-border) !important;
    box-shadow: 0 0 0 1px var(--color-primary-border) !important;
}

/* Botões */
.stButton > button {
    border-radius: var(--radius-sm) !important;
    min-height: 2.75rem;
    transition:
        background var(--dur-fast) var(--ease-out-quart),
        box-shadow var(--dur-fast) var(--ease-out-quart),
        transform var(--dur-instant) var(--ease-out-expo),
        border-color var(--dur-fast) var(--ease-out-quart),
        color var(--dur-fast) var(--ease-out-quart) !important;
}
.stButton > button[kind="primary"] {
    background: linear-gradient(180deg, var(--color-primary-bright), var(--color-primary)) !important;
    color: #ffffff !important;
    border: none !important;
    font-weight: 600 !important;
    box-shadow: 0 1px 2px rgba(230, 126, 34, 0.35);
}
.stButton > button[kind="primary"]:hover {
    background: linear-gradient(180deg, var(--color-primary), var(--color-primary-deep)) !important;
    box-shadow: 0 2px 8px rgba(230, 126, 34, 0.28);
    transform: translateY(-1px);
}
.stButton > button[kind="primary"]:active {
    transform: translateY(0) scale(0.98);
    box-shadow: 0 1px 3px rgba(230, 126, 34, 0.22) !important;
}
.stButton > button[kind="primary"]:focus-visible {
    outline: 2px solid var(--color-primary) !important;
    outline-offset: 2px !important;
}
.stButton > button[kind="secondary"]:hover {
    border-color: var(--color-primary) !important;
    color: var(--color-primary-deep) !important;
    transform: translateY(-1px);
}
.stButton > button[kind="secondary"]:active {
    transform: scale(0.98);
}
.stButton > button[kind="primary"] p { color: #ffffff !important; }

/* Inputs */
.stTextInput input, .stTextArea textarea, .stSelectbox div[data-baseweb="select"] > div {
    border-radius: var(--radius-sm) !important;
    border-color: var(--color-border) !important;
    transition:
        border-color var(--dur-fast) var(--ease-out-quart),
        box-shadow var(--dur-fast) var(--ease-out-quart) !important;
}
.stTextInput input:focus, .stTextArea textarea:focus {
    border-color: var(--color-primary) !important;
    box-shadow: 0 0 0 2px rgba(230, 126, 34, 0.18) !important;
}

/* Checklist do plano */
label[data-testid="stWidgetLabel"] + div [role="checkbox"] {
    transition: background var(--dur-fast) var(--ease-out-quart), border-color var(--dur-fast) var(--ease-out-quart) !important;
}

/* Barra de progresso Streamlit — cobre (sem verde nativo) */
div[data-testid="stProgress"] > div {
    background: var(--color-surface-muted) !important;
    border-radius: var(--radius-sm) !important;
    overflow: hidden !important;
}
div[data-testid="stProgress"] > div > div {
    background: linear-gradient(90deg, var(--color-primary-bright), var(--color-primary)) !important;
    border-radius: var(--radius-sm) !important;
    transition: width var(--dur-moderate) var(--ease-out-quart) !important;
}

/* Alertas nativos — paleta cobre */
div[data-testid="stAlert"] {
    border-radius: var(--radius-sm) !important;
}
div[data-testid="stAlert"][data-baseweb="notification"] {
    background: var(--color-info-bg) !important;
    border: 1px solid var(--color-complete-border) !important;
    color: var(--color-info-ink) !important;
}
div[data-testid="stAlert"] svg {
    color: var(--color-primary-deep) !important;
    fill: var(--color-primary-deep) !important;
}

/* Checkbox marcado — cobre */
label[data-testid="stWidgetLabel"] + div [role="checkbox"][aria-checked="true"] {
    background: var(--color-primary) !important;
    border-color: var(--color-primary-deep) !important;
}

/* Motion — keyframes (estado e feedback, sem coreografia de página) */
@keyframes painel-progresso-entra {
    from { opacity: 0.92; transform: translateY(4px); }
    to { opacity: 1; transform: translateY(0); }
}
@keyframes painel-aba-entra {
    from { opacity: 0.96; }
    to { opacity: 1; }
}
@keyframes etapa-ativa-pulso {
    0% { box-shadow: 0 0 0 0 rgba(230, 126, 34, 0.28); }
    100% { box-shadow: 0 0 0 7px rgba(230, 126, 34, 0); }
}
@keyframes pulso-indicador {
    0% { transform: scale(0.88); }
    100% { transform: scale(1); }
}
@keyframes banner-confirmacao {
    0% { opacity: 0.9; transform: scale(0.995); }
    100% { opacity: 1; transform: scale(1); }
}

hr { border-color: var(--color-border) !important; }

[data-testid="stStatusWidget"] { display: none !important; }

@media (prefers-reduced-motion: reduce) {
    *, *::before, *::after {
        animation-duration: 0.01ms !important;
        animation-iteration-count: 1 !important;
        transition-duration: 0.01ms !important;
    }
    section[data-testid="stSidebar"] { transition: none !important; }
    .stButton > button:hover,
    .stButton > button:active,
    .metric-card:hover {
        transform: none !important;
    }
    .timeline-h-item.timeline-done .timeline-h-icon {
        transform: none !important;
    }
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
    """Injeta CSS do tema claro e script de localização PT-BR."""
    import streamlit as st

    st.markdown(CSS_APP, unsafe_allow_html=True)
    if hasattr(st, "html"):
        st.html(JS_PT_BR)
    else:
        import streamlit.components.v1 as components

        components.html(JS_PT_BR, height=0, width=0)


_COR_TIPO = {
    "lideranca": "#6b4423",
    "comunicacao": "#7a4e28",
    "conflito": "#a84832",
    "desempenho": "#c76a2a",
    "processo": "#8b5a32",
    "seguranca": "#8b3a32",
}


def cor_tipo_problema(tipo: str) -> str:
    return _COR_TIPO.get((tipo or "").lower(), "#9c958e")


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
