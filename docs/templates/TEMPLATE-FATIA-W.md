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
- Pós-integração: `git revert -m 1 <merge-sha>` (reversão com commit auditável; evitar `git reset --hard`)
- Pré-integração: `git revert <commit-sha>` ou descarte da branch isolada

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
