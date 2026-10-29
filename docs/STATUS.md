# Status — DriveHub API

## 1. Último Marco Homologado e Integrado
- **Marco:** Consolidação da Clean Architecture, DDD e Endpoints de Concessionária (PR #1).
- **Data do Aceite pelo PO:** 2026-10-28 17:10:42 -0300.
- **Commit Integrado em `main`:** `829da97afe6e2237ea48b1e6ec84dd969bd262cf`.
- **Status:** HOMOLOGADO LOCALMENTE PELO PO.

---

## 2. Marco Corrente (Em Execução)
- **Marco:** W0 — Fundação e Governança do Método C.H.
- **Autonomia Autorizada:** CH-2.
- **Branch:** `metodo_ch_auditoria_w0`.
- **Baseline de Origem:** `829da97afe6e2237ea48b1e6ec84dd969bd262cf`.
- **Objetivo da W0:** Adequar o repositório às normas oficiais do Método C.H. (docs, templates, ADRs, contratos, AGENTS.md e rastreabilidade), sem alterar o comportamento funcional da aplicação.

---

## 3. Evidências Verificadas da Branch Principal (`main`)
- **Suite de Testes:** 32 testes automatizados em pytest (`pytest -v`), 100% aprovados.
- **Cobertura Funcional:** Domínio puro, use cases, integridade transacional com rollback atômico, RBAC por perfil gerencial, hardening de segurança em produção e proteção do comando de seed.
- **Segurança:** Bloqueio estrito de `seed_drivehub` em produção (`IS_PRODUCTION=True`), bloqueio de wildcards em hosts e CORS.

---

## 4. Riscos Técnicos e Ressalvas Identificadas (Para Fatias Posteriores)
1. **Concorrência e Persistência SQLite vs PostgreSQL**:
   - Em desenvolvimento local, SQLite opera com serialização a nível de arquivo/banco. O driver SQLite no Django ignora silenciosamente `SELECT ... FOR UPDATE`.
   - A preparação com PostgreSQL e concorrência baseada em MVCC/row-level lock permanece pendente no backlog de infraestrutura.
2. **Lacuna de Autenticação na Integração Frontend-Backend**:
   - A API exige `IsManager` (usuário autenticado com perfil gerencial) para as ações `/sales/proposals/:id/approve/` e `/sales/proposals/:id/complete/`.
   - O frontend `DriveHub-Web` atualmente realiza chamadas unauthenticated, o que gerará respostas HTTP 401/403 até que a camada de autenticação (JWT / Sessão) seja implementada na esteira de fatias.
3. **Ambiente de Produção**:
   - O projeto está validado para desenvolvimento local. Parâmetros de produção exigem configuração segura de segredos em cofre externo.

---

## 5. Próximo Marco
- **Fatia W1:** Autenticação e Contrato Integrado Full-Stack (Login, Token JWT/Sessão e Conexão Frontend-Backend).
