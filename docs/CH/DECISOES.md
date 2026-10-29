# Índice de Decisões Arquiteturais e de Governança — DriveHub-API

> **Nota Epistêmica:** Este índice distingue formalmente decisões governadas sob o Método C.H. (com evidência documental e rastreabilidade por Fatia W) de decisões técnicas históricas adotadas antes da institucionalização do método. Decisões pré-C.H. são registradas como baseline factual, sem atribuição de homologação retroativa.

---

## 1. Decisões Formais sob Governança do Método C.H.

| ID | Data | Decisão | Fonte / Evidência | Estado C.H. | Decisor |
|---|---|---|---|---|---|
| ADR-0001 | 2026-10-29 | Adoção formal do Método Ágil C.H. e Clean Architecture como padrão de governança | PR #2 / Squash `a88be75b1d6084e95801b4e7c18500126f29d32f` | HOMOLOGADA | PO Hallan |
| D-0002 | 2026-10-29 | Delimitação de escopo, contratos full-stack e catálogo de riscos técnicos da W0 sem mutação de código de negócio | `docs/CH/W0-GOVERNANCA.md` / PR #2 | HOMOLOGADA | PO Hallan |
| D-0005 | 2026-10-29 | Homologação final e integração da Fatia W0 na branch `main` via Squash Merge | PR #2 / Commit `a88be75b1d6084e95801b4e7c18500126f29d32f` | HOMOLOGADA | PO Hallan |
| D-0006 | 2026-10-29 | Implantação de workflow de CI automatizado (`.github/workflows/ci.yml`) e proposta de ruleset para a branch `main` | `docs/CH/W0.1-GOVERNANCA.md` / Issue #3 | PROPOSTA (W0.1) | Orquestrador / PO |

---

## 2. Decisões Técnicas Históricas (Pré-Método C.H. / Baseline do Projeto)

> Decisões arquiteturais e de implementação integradas na branch `main` antes do início formal da governança C.H. Não possuem RUC ou homologação retroativa sob as normas C.H.; representam o estado factual herdado pelo projeto.

| ID | Data da Integração | Decisão Técnica Histórica | Fonte / Referência Git | Estado Factual |
|---|---|---|---|---|
| HIST-001 | 2026-10-28 | Migração arquitetural para Clean Architecture e Domain-Driven Design (DDD) com Django 5 e DRF | PR #1 / Merge `829da97afe6e2237ea48b1e6ec84dd969bd262cf` | HISTORICA_INTEGRADA |
| HIST-002 | 2026-10-28 | Hardening do comando `seed_drivehub` com geração de senhas aleatórias seguras e bloqueio em produção | PR #1 (`tests/integration/test_security_hardening.py`) | HISTORICA_INTEGRADA |
| HIST-003 | 2026-10-28 | Controle de acesso por perfil (RBAC) com permissão `IsManager` em aprovação e conclusão de vendas | PR #1 (`apps/sales/permissions.py`) | HISTORICA_INTEGRADA |
| HIST-004 | 2026-10-28 | Transações atômicas com `@transaction.atomic` em operações mutatórias de múltiplos agregados | PR #1 (`apps/sales/views.py`) | HISTORICA_INTEGRADA |
| HIST-005 | 2026-10-28 | Adoção de `select_for_update()` na camada de repositório como preparação para PostgreSQL alvo | PR #1 (`apps/vehicles/repositories.py`) | HISTORICA_INTEGRADA |
