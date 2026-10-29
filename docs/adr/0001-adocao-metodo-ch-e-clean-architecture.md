# ADR-0001 — Adoção do Método C.H. e Clean Architecture no Backend

- **Data:** 2026-10-29
- **Estado:** Proposta (Aguardando homologação e aceite do PO na W0)
- **Decisor:** Product Owner (Hallan)

---

## 1. Contexto
A API do DriveHub evoluiu de um protótipo monolítico simples para uma plataforma corporativa de concessionária, demandando separação rigorosa de regras de negócio, auditoria de hodômetro, controle de alçadas de desconto e esteira de vendas. Era necessário padronizar a governança de engenharia com agentes autônomos e garantir previsibilidade arquitetural.

---

## 2. Decisão
1. **Governança:** Adoção oficial do **Método Ágil C.H. (Colaboração Híbrida)**, dividindo o ciclo de entrega em fases CHAVE e Fatias W com autonomia calibrada (CH-0 a CH-3) e gates de evidências verificáveis.
2. **Padrão Arquitetural:** Formalização da **Clean Architecture** e **Domain-Driven Design (DDD)** com segregação explícita entre Domínio puro (`core/domain`), Casos de Uso (`core/use_cases`) e Infraestrutura Django (`apps/`).
3. **Persistência:** Suporte a SQLite em desenvolvimento com preparação arquitetural para PostgreSQL com MVCC em produção via `select_for_update()`.
4. **Controle de Acesso:** Manutenção da política RBAC via permissão `IsManager` nas ações de maior sensibilidade negocial (`approve` e `complete`).

---

## 3. Consequências

### Positivas
- Regras de domínio e casos de uso tornam-se 100% testáveis com fakes em memória, sem acoplamento ao ORM ou banco de dados.
- O ciclo de vida de propostas e estoques obedece a invariantes rígidas e transações atômicas com rollback garantido.
- Governança clara para colaboração híbrida humano-IA, evitando alucinações e mutações descontroladas no repositório.

### Trade-offs & Limitações
- Maior verbosidade e número de arquivos comparado ao padrão Django tradicional.
- Necessidade de mapeamento explícito entre entidades de domínio e models do Django ORM nos repositórios.
- Operações que exigem `IsManager` demandam integração com camada de autenticação no frontend (a ser concluída em fatia posterior).
