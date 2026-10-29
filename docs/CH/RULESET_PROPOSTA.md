# Proposta de Proteção de Branch e Ruleset — DriveHub-API

> **Norma Canônica:** Método Ágil C.H. ([hallanbrito/metodo-ch](https://github.com/hallanbrito/metodo-ch))  
> **Fatia:** W0.1 — Blindagem de Governança e CI  
> **Data:** 2026-10-29  
> **Estado:** Proposta para Deliberação do PO (Não aplicada automaticamente)

---

## 1. Diagnóstico do Estado Atual
- **Visibilidade do Repositório:** `PUBLIC` (GitHub Free/Open Source).
- **Branch Principal:** `main`.
- **Proteção Atual:** Nenhuma proteção ativa (`Branch not protected` / `rulesets: []`).
- **Riscos Identificados:**
  - Possibilidade de commits diretos na branch `main` sem revisão.
  - Possibilidade de force push acidental (`git push --force`), com potencial de perda do histórico auditável.
  - Possibilidade de deleção da branch principal.
  - Ausência de validação automatizada pré-merge como requisito impeditivo.

---

## 2. Diretrizes da Proposta de Governança
1. **Exigência de Pull Request:**
   - Todo código deve passar obrigatoriamente por Pull Request antes de ser integrado na `main`.
   - Exigência de no mínimo 1 aprovação formal pelo Product Owner (`hallanbrito`).
   - Descarte automático de aprovações antigas em caso de novos commits (`dismiss_stale_reviews_on_push: true`).
   - Exigência de encerramento de todas as conversas/tópicos de revisão (`required_review_thread_resolution: true`).
2. **Bloqueio de Comandos Destrutivos:**
   - Bloqueio absoluto de deleção de branch (`deletion: true`).
   - Bloqueio absoluto de push forçado (`non_fast_forward: true`).
3. **Status Checks Obrigatórios:**
   - Apenas checks comprovadamente operacionais e que já passem na esteira:
     - Check: `Django Checks & Pytest (Python 3.12)` (oriundo do workflow `.github/workflows/ci.yml`).
   - Não exigir status checks não operacionais ou inexistentes.
4. **Bypass Mínimo e Estrito:**
   - Restrito exclusivamente a usuários com papel de `Repository Admin` (PO Hallan), para situações excepcionais de recuperação ou governança, preservando registro no audit log do GitHub.

---

## 3. Especificação do Ruleset (JSON para Aplicação)

Para aplicar este ruleset, o PO pode utilizar o comando abaixo via GitHub CLI após autorização formal:

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
        "required_approving_review_count": 1,
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

---

## 4. Próximos Passos
- Esta proposta é documental e não foi aplicada administrativamente pelo agente (em estrito cumprimento ao princípio da autorização administrativa).
- Aguarda deliberação e aplicação manual pelo PO Hallan.
