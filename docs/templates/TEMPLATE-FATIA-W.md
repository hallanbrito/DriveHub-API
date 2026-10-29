# W__ — <Título Curto da Fatia>

## Identidade
- **Objetivo:**
- **Valor esperado:**
- **Responsável humano (PO):** Hallan
- **Orquestrador:** ChatGPT
- **Executor:**
- **Nível de autonomia:** CH-0 / CH-1 / CH-2 / CH-3

---

## C — Contextualizar
- **Baseline (branch/commit SHA):**
- **Fonte de verdade consultada:**
- **Estado atual:**
- **Riscos conhecidos:**

---

## H — Harmonizar

### Escopo autorizado
-

### Fora do escopo
-

### Decisões aprovadas
-

### Decisões ainda proibidas / abertas
-

### Critérios de aceitação verificáveis
- [ ] T01:

### Estratégia de reversão auditável
- **Pós-integração (conforme método de merge utilizado):**
  - *Caso A — Merge Commit:* `git revert -m 1 <merge-commit-sha>` (confirmar previamente os pais e direção)
  - *Caso B — Squash Merge:* `git revert <squash-commit-sha>` (sem flag `-m`, commit de pai único)
  - *Caso C — Rebase Merge:* Reversão ordenada e individual dos commits lineares identificados (`git revert <sha>`)
- **Pré-integração:** `git revert <commit-sha>` ou descarte da branch isolada
- **Diretrizes gerais:**
  - Reversão pós-integração deve tramitar via branch isolada e Pull Request (sem push direto na `main`), sujeita aos gates de CI e aceite formal do PO.
  - Nunca aplicar `git reset --hard` à `main` como procedimento de rollback.
  - Exigir árvore limpa e autorização explícita do PO antes de executar reversão real.
  - Validar a aplicação (testes/build) e registrar evidências após o rollback.

---

## A — Agir
- **Ambiente isolado (branch/worktree):**
- **Ferramentas / acessos autorizados:**
- **Condição de parada:**

---

## V — Verificar
- [ ] Diff revisado linha a linha
- [ ] Testes automatizados executados e aprovados
- [ ] Aderência ao escopo confirmada
- [ ] Segurança e dependências avaliadas
- [ ] Limitações e não-testados declarados
- [ ] Pacote de Evidências completo

---

## E — Evoluir
- **Decisão humana:** Aceitar / Corrigir / Rejeitar
- **Integração:** PENDENTE DE ACEITE DO PO
- **Aprendizado devolvido à memória versionada:**
