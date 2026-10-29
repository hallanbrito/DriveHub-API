# Status — DriveHub API

## 1. Último Marco Homologado e Integrado sob o Método C.H.
- **Marco:** W0 — Fundação e Governança do Método C.H.
- **Data do Aceite pelo PO:** 2026-10-29.
- **Commit Integrado em `main` (Squash Merge):** `a88be75b1d6084e95801b4e7c18500126f29d32f`.
- **Pull Request:** [#2](https://github.com/hallanbrito/DriveHub-API/pull/2) (Merged).
- **Status Factual:** HOMOLOGADO E INTEGRADO EM MAIN PELO PO.

---

## 2. Marco Histórico do Projeto (Pré-Método C.H.)
- **Marco Histórico:** Consolidação da Clean Architecture, DDD e Endpoints de Concessionária (PR #1).
- **Data da Integração:** 2026-10-28 17:10:42 -0300.
- **Commit Integrado em `main`:** `829da97afe6e2237ea48b1e6ec84dd969bd262cf`.
- **Status Factual:** Baseline técnico inicial integrado na branch `main`.

---

## 3. Marco Corrente do Método C.H. (Fatia W0.1 — Em Execução)
- **Marco:** W0.1 — Blindagem de Governança e CI.
- **Autonomia Autorizada:** CH-2.
- **Issue Vinculada:** [#3](https://github.com/hallanbrito/DriveHub-API/issues/3).
- **Branch de Trabalho:** `agy/w0-1-governanca-ci`.
- **Baseline de Origem:** `a88be75b1d6084e95801b4e7c18500126f29d32f`.
- **Objetivo da W0.1:** Implantar workflow de CI executável (`.github/workflows/ci.yml`), proposta formal de ruleset para a branch `main` e rastreabilidade da governança.
- **Estado Atual da W0.1:** EM EXECUÇÃO / AGUARDANDO REVISÃO DO ORQUESTRADOR E ACEITE DO PO.

---

## 4. Evidências Verificadas da Branch Principal (`main`)
- **Suite de Testes:** 32 testes automatizados em pytest (`pytest -v`), 100% aprovados.
- **Validação Django:** `python manage.py check` com 0 apontamentos.
- **Cobertura Funcional:** Domínio puro, use cases, integridade transacional com rollback atômico, RBAC por perfil gerencial, hardening de segurança em produção e proteção do comando de seed.
- **Segurança:** Bloqueio estrito de `seed_drivehub` em produção (`IS_PRODUCTION=True`), bloqueio de wildcards em hosts e CORS.

---

## 5. Riscos Técnicos e Limitações Catalogadas (Para Fatias Posteriores)
1. **Proteção da Branch `main` Não Ativada**:
   - Atualmente a branch `main` está desprotegida no GitHub.
   - Proposta formal de ruleset elaborada em `docs/CH/RULESET_PROPOSTA.md` aguardando ativação administrativa pelo PO Hallan.
2. **Concorrência e Persistência SQLite vs PostgreSQL**:
   - Em desenvolvimento local, SQLite opera com serialização a nível de arquivo/banco. O driver SQLite no Django ignora silenciosamente `SELECT ... FOR UPDATE`.
   - A preparação com PostgreSQL e concorrência baseada em MVCC/row-level lock permanece pendente no backlog de infraestrutura.
3. **Lacuna de Autenticação na Integração Frontend-Backend**:
   - A API exige `IsManager` (usuário autenticado com perfil gerencial) para as ações `/sales/proposals/:id/approve/` e `/sales/proposals/:id/complete/`.
   - O frontend `DriveHub-Web` atualmente realiza chamadas unauthenticated.
4. **Ambiente de Produção**:
   - O projeto está validado para desenvolvimento local. Parâmetros de produção exigem configuração segura de segredos em cofre externo.

---

## 6. Próximo Marco
- **Fatia W1:** Autenticação e Contrato Integrado Full-Stack (Login, Token JWT/Sessão e Conexão Frontend-Backend).
