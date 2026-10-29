# Proposta de Proteção de Branch e Ruleset — DriveHub-API

> **Norma Canônica:** Método Ágil C.H. ([hallanbrito/metodo-ch](https://github.com/hallanbrito/metodo-ch))  
> **Fatia:** W0.1 — Blindagem de Governança e CI  
> **Data:** 2026-10-29  
> **Estado:** Proposta para Deliberação do PO (Não aplicada automaticamente)

---

## 1. Diagnóstico do Estado Atual
- **Visibilidade do Repositório:** `PUBLIC` (GitHub Free / Open Source).
- **Branch Principal:** `main`.
- **Proteção Atual:** Nenhuma proteção ativa (`Branch not protected` / `rulesets: []`).
- **Riscos Identificados:**
  - Possibilidade de commits diretos na branch `main` sem revisão.
  - Possibilidade de force push acidental (`git push --force`), com potencial de perda do histórico auditável.
  - Possibilidade de deleção da branch principal.
  - Ausência de validação automatizada pré-merge como requisito impeditivo.

---

## 2. Segregação Explícita dos Quatro Pilares de Governança

Para evitar impasses operacionais ou regras impossíveis de satisfazer, a governança do repositório distingue rigorosamente quatro dimensões:

### Pilar 1: Revisão Técnica Independente
- **Ator:** Orquestrador Cognitivo (ChatGPT), agentes de auditoria ou revisores técnicos pares.
- **Natureza:** Análise técnica da solução, integridade da suite de testes, conformidade de arquitetura e ausência de regressões.
- **Materialização:** Parecer técnico formal registrado nos comentários do Pull Request e no Pacote de Evidências / RUC. Não depende de permissões administrativas no repositório.

### Pilar 2: Aceite Formal do Product Owner (PO)
- **Ator:** Product Owner (`hallanbrito` / Hallan).
- **Natureza:** Decisão humana soberana e indelegável sobre valor de negócio e cumprimento dos critérios de aceitação da Fatia W.
- **Materialização:** Declaração explícita de homologação registrada no PR ou na issue (ex: *"Fatia W0.1 aceita formalmente"*). Precede obrigatoriamente a integração.

### Pilar 3: Mecanismo de Aprovação de Pull Request na Plataforma GitHub
- **Regra Nativa da Plataforma:** O GitHub bloqueia categoricamente autores de aprovarem seus próprios Pull Requests (*"Pull request authors cannot approve their own pull requests"*).
- **Análise de Contexto:** Quando o PO (`hallanbrito`) é o próprio autor do PR (ou quando ferramentas agênticas submetem PRs autenticadas via credenciais/CLI do PO), configurar `required_approving_review_count: 1` no GitHub impede o merge legítimo pela própria interface, forçando o uso indevido de bypass.
- **Diretriz de Configuração do Ruleset:**
  - **Configuração Recomendada (Mantenedor Único / Autor-PO):**
    - Configurar `required_approving_review_count: 0`.
    - Manter exigência estrita de Pull Request (bloqueia push direto na `main`).
    - Exigir resolução obrigatória de tópicos de revisão (`required_review_thread_resolution: true`).
    - Exigir **Status Check Obrigatório** verde (`Django Checks & Pytest (Python 3.12)`).
    - O controle humano do PO é garantido pelo ato soberano de autorizar e acionar o botão de merge do PR, mantendo o processo 100% auditável sem exigir bypass.
  - **Configuração Alternativa (Multi-Ator / Bot Agêntico com Conta Própria):**
    - Caso os agentes operem via GitHub App dedicada ou haja um segundo desenvolvedor humano cadastrado no repositório, `required_approving_review_count` pode ser configurado como `1`.

### Pilar 4: Bypass Administrativo Excepcional
- **Ator:** `Repository Admin` (PO Hallan).
- **Natureza:** Mecanismo estritamente reservado para contingências críticas e recuperação de desastres (ex.: indisponibilidade do runner do GitHub Actions, necessidade urgente de hotfix de infraestrutura).
- **Diretriz de Uso:** **Vedado como fluxo normal ou rotineiro de integração.** Qualquer utilização de bypass deve ser acompanhada de justificativa formal registrada no RUC e fica gravada no audit log da organização.

---

## 3. Especificação do Ruleset (JSON para Aplicação)

### Modelo Recomendado (Mantenedor Único / Autor-PO):
Configuração que protege a `main`, exige PR e testes automatizados sem bloquear o autor-PO:

```bash
gh api --method POST repos/hallanbrito/DriveHub-API/rulesets \
  --input - << 'EOF'
{
  "name": "drivehub-api-main-protection",
  "target": "branch",
  "enforcement": "active",
  "conditions": {
    "ref_name": {
      "include": [
        "~DEFAULT_BRANCH"
      ],
      "exclude": []
    }
  },
  "rules": [
    {
      "type": "pull_request",
      "parameters": {
        "required_approving_review_count": 0,
        "dismiss_stale_reviews_on_push": true,
        "require_code_owner_review": false,
        "require_last_push_approval": false,
        "required_review_thread_resolution": true
      }
    },
    {
      "type": "deletion"
    },
    {
      "type": "non_fast_forward"
    },
    {
      "type": "required_status_checks",
      "parameters": {
        "strict_required_status_checks_policy": true,
        "required_status_checks": [
          {
            "context": "Django Checks & Pytest (Python 3.12)"
          }
        ]
      }
    }
  ],
  "bypass_actors": [
    {
      "actor_id": 1,
      "actor_type": "RepositoryRole",
      "bypass_mode": "always"
    }
  ]
}
EOF
```

> **Nota:** Caso o repositório passe a contar com conta agêntica autônoma (GitHub App) ou co-revisor técnico humano, alterar o parâmetro `"required_approving_review_count": 1` para habilitar a aprovação formal na interface do GitHub por terceiros.

---

## 4. Próximos Passos
- Esta proposta é de natureza estritamente documental e consultiva (CH-1 / CH-2 isolado), não tendo sido aplicada administrativamente pelo agente executor.
- Aguarda deliberação e eventual aplicação manual pelo PO Hallan.
