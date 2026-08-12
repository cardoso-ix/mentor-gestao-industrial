# Portfólio — Eduardo Cardoso

Portfólio pessoal em HTML, CSS e JavaScript vanilla. Site de uma página, responsivo, com tema claro/escuro, deploy via **GitHub Pages**.

**Posicionamento:** perfil universal de **suporte técnico** e **automações com IA** (n8n, OpenAI, APIs) — mostra competências na prática, sem tom de anúncio de vaga.

**Live:** [cardoso-ix.github.io/Portifolio](https://cardoso-ix.github.io/Portifolio/)

## Stack

| Camada | Tecnologia |
|--------|------------|
| Site principal | HTML5, CSS3, JavaScript (vanilla) |
| Fontes | Inter + JetBrains Mono (Google Fonts) |
| Visual | Graphite + oliva (`#a8b87a`), layout centralizado (`88rem`) |
| Subprojeto embarcado | React + Vite (build em `conversor-unidades/`) |
| Scripts auxiliares | Python 3 — Pillow, ReportLab |
| CI | GitHub Actions — verificação de links (Lychee) + HTML validate |
| Deploy | GitHub Pages (`main` → `/`) |

## Estrutura

```
Portifolio/
├── index.html
├── css/style.css
├── js/main.js
├── assets/
│   ├── cv_eduardo_cardoso.pdf
│   ├── favicon-*.png / favicon.svg / apple-touch-icon.png
│   └── images/
│       ├── foto.png              # hero + JSON-LD
│       ├── foto-cv.png           # foto do currículo
│       ├── og-image.png
│       ├── linkedin-banner.png
│       └── *-preview.*           # previews dos projetos
├── conversor-unidades/
├── scripts/
│   ├── generate_cv.py
│   ├── generate_favicon.py
│   ├── generate_og_image.py
│   ├── generate_linkedin_banner.py
│   ├── gen_pc_dashboard_preview.py
│   ├── font_utils.py
│   ├── format_html.py
│   └── requirements.txt
├── docs/
│   ├── PROJETOS-GITHUB.md
│   ├── LINKEDIN-PERFIL.md
│   └── AVALIACAO-PERFIL.md
├── robots.txt
├── sitemap.xml
├── site.webmanifest
├── 404.html
├── PRODUCT.md
├── DESIGN.md
├── .github/workflows/check-links.yml
└── .cursor/                   # regras do Cursor (opcional)
```

## Projetos em destaque no site

Inventário completo: [docs/PROJETOS-GITHUB.md](docs/PROJETOS-GITHUB.md).

| Projeto | Demo | Código |
|---------|------|--------|
| Automação LinkedIn com IA | [LinkedIn](https://www.linkedin.com/in/eduardo-cardoso-213a02267) | [GitHub](https://github.com/cardoso-ix/linkedin-automacao-ia) — Hermes + DeepSeek-V4-Flash + replies automáticos |
| PC Dashboard | — (Windows · Tauri v1.4) | [GitHub](https://github.com/cardoso-ix/pc-dashboard) |
| Mentor de Gestão Industrial | [Testar demo](https://huggingface.co/spaces/duzinxd/mentor-gestao-industrial) | [GitHub](https://github.com/cardoso-ix/mentor-gestao-industrial) — CrewAI · OpenCode Go · DeepSeek V4 Flash · RAG |
| Conversor de Unidades | [GitHub Pages](https://cardoso-ix.github.io/Portifolio/conversor-unidades/) | [GitHub](https://github.com/cardoso-ix/conversor-unidades) |

Outros repos públicos: `cardoso-ix` (README do perfil).

## Seções do site

1. **Início** — hero (suporte técnico + automações/IA), terminal, CTAs (projetos, currículo, contato)
2. **Projetos** — 1 destaque + grade compacta
3. **Sobre** — trajetória, como trabalha, Pós Tech em Agentes de IA
4. **Skills** — em uso, complementares, estudando, soft skills
5. **Formação** — timeline acadêmica
6. **Experiência** — histórico profissional (antigo colapsável)
7. **Contato** — WhatsApp, e-mail, LinkedIn, GitHub, currículo

## Visualizar localmente

```bash
python -m http.server 8000
```

Acesse `http://localhost:8000`. O conversor embarcado funciona em `http://localhost:8000/conversor-unidades/`.

## Scripts Python

```bash
pip install -r scripts/requirements.txt
python scripts/generate_cv.py
python scripts/generate_favicon.py
python scripts/generate_og_image.py
python scripts/generate_linkedin_banner.py
python scripts/gen_pc_dashboard_preview.py
python scripts/format_html.py
```

## Trocar foto de perfil

1. Substitua `assets/images/foto.png` (site) e `assets/images/foto-cv.png` (currículo).  
2. Rode `python scripts/generate_cv.py` e `python scripts/generate_og_image.py`.  
3. Incremente `?v=` nos links da foto/PDF em `index.html`.  
4. Publique na `main` (GitHub Pages).

## SEO e qualidade

- **Open Graph** — `assets/images/og-image.png` (1200×630)
- **JSON-LD** — schema `Person` em `index.html`
- **robots.txt** + **sitemap.xml**
- **404.html** — página de erro no GitHub Pages
- **site.webmanifest** — metadados PWA básicos
- **CI** — links (Lychee) + validação HTML

## Documentação

| Arquivo | Conteúdo |
|---------|----------|
| [PRODUCT.md](PRODUCT.md) | Propósito, público, princípios e fontes de verdade |
| [DESIGN.md](DESIGN.md) | Sistema visual Quiet Graphite Olive (cores, tipografia, componentes) |
| [docs/PROJETOS-GITHUB.md](docs/PROJETOS-GITHUB.md) | Inventário dos repositórios públicos e demos |
| [docs/AVALIACAO-PERFIL.md](docs/AVALIACAO-PERFIL.md) | Avaliação do posicionamento e próximos passos |
| [docs/LINKEDIN-PERFIL.md](docs/LINKEDIN-PERFIL.md) | Kit LinkedIn (capa, headline, Sobre, experiências) |
| [.cursor/rules/portfolio.mdc](.cursor/rules/portfolio.mdc) | Convenções para edição no Cursor |

## Publicar

Repositório: [`cardoso-ix/Portifolio`](https://github.com/cardoso-ix/Portifolio). Push na `main` atualiza o GitHub Pages.

Após alterar CSS, JS, PDF ou foto, incremente `?v=` nos links em `index.html`.

## Licença

Uso livre para fins pessoais e educacionais.
