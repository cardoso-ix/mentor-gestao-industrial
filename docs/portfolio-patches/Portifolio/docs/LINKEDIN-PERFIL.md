# LinkedIn — kit para copiar e colar

Atualizado: jul/2026.

Tudo abaixo está alinhado ao portfólio publicado, ao currículo real e aos repositórios GitHub.  
**Não invente** formação, empresa ou ferramenta fora desta lista.  
Inventário completo: [PROJETOS-GITHUB.md](./PROJETOS-GITHUB.md).

Portfólio: https://cardoso-ix.github.io/Portifolio/  
Currículo PDF: https://cardoso-ix.github.io/Portifolio/assets/cv_eduardo_cardoso.pdf

Ordem sugerida no LinkedIn: Foto → Capa → Headline → Sobre → Experiência → Formação → Featured → Skills.

---

## 0) Foto de perfil

Use a mesma foto do portfólio (rosto bem enquadrado).

- Arquivo no site: `assets/images/foto.png`  
- URL: https://cardoso-ix.github.io/Portifolio/assets/images/foto.png  

Ao trocar a foto no LinkedIn, atualize também `foto.png` + `foto-cv.png` no repositório e regenere OG/CV se necessário.

---

## 1) Capa (banner) — arquivo pronto

Arquivo gerado no tamanho recomendado do LinkedIn (**1584 × 396**):

- No repositório: `assets/images/linkedin-banner.png`
- URL (após publish): https://cardoso-ix.github.io/Portifolio/assets/images/linkedin-banner.png

**Como usar**
1. LinkedIn → foto da capa → Editar  
2. Enviar `linkedin-banner.png`  
3. Ajustar o enquadramento (o texto fica à **direita**; a foto de perfil cobre o canto inferior esquerdo)

Para regenerar: `python3 scripts/generate_linkedin_banner.py`

Identidade da capa: graphite + oliva do portfólio · suporte técnico · n8n / OpenAI / Help Desk · sem “busco vaga”.

---

## 2) Headline (cargo sob o nome)

Cole exatamente:

```
Suporte técnico · Automações com IA | n8n · OpenAI · Help Desk · Chapecó, SC
```

Alternativa (se preferir mais curta):

```
Suporte técnico e automações com IA | n8n · OpenAI · APIs
```

---

## 3) Sobre (About)

Cole exatamente:

```
Trabalho na interseção de suporte técnico e automações com IA: entender o problema do usuário, diagnosticar, resolver e — quando faz sentido — automatizar com n8n, OpenAI e APIs.

Tenho experiência em Help Desk (Crescer Sistemas): atendimento a chamados técnicos (N1/N2), diagnóstico e resolução de software e hardware, suporte remoto e presencial. Essa base de atendimento e diagnóstico eu aplico hoje em fluxos e integrações que reduzem retrabalho.

Projetos em destaque:
• Automação de publicações no LinkedIn (Hermes + DeepSeek-V4-Flash) — post diário com texto validado e foto própria; respostas automáticas a comentários via API LinkedIn
• PC Dashboard — painel Windows (Tauri) com ações de um clique, bandeja e remoção de programas
• Mentor de Gestão Industrial — multi-agente CrewAI + OpenCode Go (DeepSeek V4 Flash) + RAG (demo no Hugging Face)
• Conversor de Unidades — app web React + TypeScript (49 categorias)

Stack: n8n · OpenAI / APIs · Python · HTML/CSS/JS · Git/GitHub

Formação: Administração (Universidade de Franca) · MBA em Controladoria e Finanças (Cruzeiro do Sul) · Técnico em Automação Industrial (SENAI) · Pós Tech em Agentes de IA (FIAP + Alura, em andamento)

Chapecó, SC
Portfólio: https://cardoso-ix.github.io/Portifolio/
```

---

## 4) Experiência — um bloco por cargo

Use **título e empresa exatamente** como abaixo. Em cada cargo, cole a descrição na caixa “Descrição”.

### 4.1 Técnico de Laboratório de Calibração — Fluxo Metrologia

- **Cargo:** Técnico de Laboratório de Calibração  
- **Empresa:** Fluxo Metrologia  
- **Local:** Chapecó, Santa Catarina, Brasil  
- **Período:** jul de 2025 — o momento (atual)  
- **Descrição:**

```
Calibração de instrumentos de medição, emissão de certificados, gestão de padrões de referência e conformidade documental conforme normas de qualidade.
```

### 4.2 Coordenador de Logística — Sandimas

- **Cargo:** Coordenador de Logística  
- **Empresa:** Sandimas  
- **Local:** Chapecó, Santa Catarina, Brasil  
- **Período:** mai de 2023 — fev de 2025  
- **Descrição:**

```
Planejamento, coordenação e controle das operações logísticas: transporte, armazenagem, distribuição e controle de estoque, com foco em eficiência, cumprimento de prazos e redução de custos operacionais.
```

### 4.3 Suporte Técnico Help Desk — Crescer Sistemas

- **Cargo:** Suporte Técnico Help Desk  
- **Empresa:** Crescer Sistemas  
- **Local:** Chapecó, Santa Catarina, Brasil  
- **Período:** fev de 2022 — mai de 2023  
- **Descrição:**

```
Atendimento a chamados técnicos (N1/N2): diagnóstico e resolução de problemas de software e hardware, suporte remoto e presencial aos usuários, com comunicação clara e foco na resolução.
```

### 4.4 Orçamentista — MR Indústria Gráfica

- **Cargo:** Orçamentista  
- **Empresa:** MR Indústria Gráfica  
- **Local:** Concórdia, Santa Catarina, Brasil  
- **Período:** out de 2020 — jun de 2021  
- **Descrição:**

```
Análise de solicitações de clientes e elaboração de orçamentos de produtos gráficos, considerando custos de materiais, processos de impressão, acabamentos e prazos de produção.
```

### 4.5 Metrologista — JBS Foods

- **Cargo:** Metrologista  
- **Empresa:** JBS Foods  
- **Local:** Jacarezinho, Paraná, Brasil  
- **Período:** dez de 2014 — dez de 2019  
- **Descrição:**

```
Garantia da confiabilidade dos processos de medição: execução de calibrações, gestão de padrões de referência e manutenção da rastreabilidade metrológica.
```

---

## 5) Formação (Educação)

### 5.1 Pós Tech em Agentes de IA — FIAP + Alura

- **Curso:** Pós Tech em Agentes de IA  
- **Instituição:** FIAP (parceria Alura)  
- **Período:** jun de 2026 — em andamento  

### 5.2 MBA em Controladoria e Finanças — Cruzeiro do Sul

- **Curso:** MBA em Controladoria e Finanças  
- **Instituição:** Universidade Cruzeiro do Sul  
- **Período:** 2022  

### 5.3 Administração — Universidade de Franca

- **Curso:** Administração  
- **Instituição:** Universidade de Franca (UNIFRAN)  
- **Período:** 2016 — 2020  

### 5.4 Indicadores de Pesagem e Normalização — INMETRO

- **Curso:** Indicadores de Pesagem e Normalização  
- **Instituição:** INMETRO  
- **Período:** 2014  

### 5.5 Técnico em Automação Industrial — SENAI

- **Curso:** Técnico em Automação Industrial  
- **Instituição:** SENAI — Santo Antônio da Platina  
- **Período:** 2010 — 2012  

---

## 6) Em destaque (Featured) — links

Adicione nesta ordem:

1. **Portfólio** — https://cardoso-ix.github.io/Portifolio/  
2. **Automação LinkedIn (GitHub)** — https://github.com/cardoso-ix/linkedin-automacao-ia  
3. **Mentor — testar demo** — https://huggingface.co/spaces/duzinxd/mentor-gestao-industrial  
4. **Currículo (PDF)** — https://cardoso-ix.github.io/Portifolio/assets/cv_eduardo_cardoso.pdf  
5. **PC Dashboard (opcional)** — https://github.com/cardoso-ix/pc-dashboard  

---

## 7) Competências (Skills) — ordem sugerida

Adicione e pin as primeiras:

1. Help Desk  
2. Suporte Técnico  
3. n8n  
4. OpenAI  
5. Automação de Processos  
6. APIs  
7. Integrações  
8. Python  
9. Prompt Engineering  
10. HTML  
11. CSS  
12. JavaScript  
13. Git  
14. Diagnóstico de software e hardware  
15. Atendimento ao usuário  

---

## 8) Informações do perfil

| Campo | Valor |
|-------|--------|
| Nome | Eduardo Cardoso |
| Localização | Chapecó, Santa Catarina, Brasil |
| Site | https://cardoso-ix.github.io/Portifolio/ |
| E-mail | eduardoocardosoo@gmail.com |
| WhatsApp | +55 49 99809-5955 |
| GitHub | https://github.com/cardoso-ix |

---

## Checklist rápido

- [ ] Foto de perfil alinhada ao portfólio  
- [ ] Capa `linkedin-banner.png` enviada  
- [ ] Headline colada  
- [ ] Sobre colado (projetos reais do GitHub)  
- [ ] 5 experiências com título/empresa/período/descrição corretos  
- [ ] 5 formações corretas  
- [ ] Featured com site + LinkedIn automation + Mentor demo + PDF  
- [ ] Skills priorizadas  
- [ ] Sem “busco vaga / CLT / freela” no título  
- [ ] Sem UNOESC, Unimed ou qualquer dado fora deste documento  
- [ ] Bio do GitHub sem “Buscando oportunidade júnior” (pendência no perfil github.com)  
