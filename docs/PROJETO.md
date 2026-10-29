# Projeto — DriveHub API

## 1. Visão e Valor
O **DriveHub** é uma solução corporativa para concessionárias de veículos de alto padrão e showrooms automotivos. A **DriveHub API** provê o núcleo de regras de negócio, governança de estoque, esteira de propostas de venda, alçadas de desconto e auditoria de veículos.

- **Product Owner:** Hallan
- **Orquestrador:** ChatGPT
- **Metodologia:** Método Ágil C.H. (Colaboração Híbrida)
- **Fonte Normativa:** [hallanbrito/metodo-ch](https://github.com/hallanbrito/metodo-ch)

---

## 2. Arquitetura Atual
- **Linguagem & Framework:** Python 3.14 + Django 5.2 + Django REST Framework.
- **Padrão Arquitetural:** Clean Architecture e Domain-Driven Design (DDD).
  - `core/domain/`: Entidades puras independentes de frameworks (`Vehicle`, `Brand`, `SaleProposal`), Enums (`VehicleStatus`, `PaymentMethod`, `ProposalStatus`), exceções de domínio e interfaces de repositórios.
  - `core/use_cases/`: Casos de uso desacoplados de persistência (`vehicles.py`, `sales.py`).
  - `apps/vehicles/` e `apps/sales/`: Camada de infraestrutura e adaptadores Django (models, serializers, repositórios concretos e views/viewsets).
  - `app/`: Configurações centrais, settings rigorosos e rotas OpenAPI via `drf-spectacular`.
  - `tests/`: Testes automatizados unitários (`tests/unit/`) e de integração (`tests/integration/`).

---

## 3. Principais Invariantes de Negócio
1. **Governança de Descontos**:
   - Até 5%: Aprovação automática.
   - De 5,01% a 15%: Exige aprovação de Gerente (`PENDING_MANAGER`).
   - Acima de 15%: Rejeitado imediatamente pelo domínio.
2. **Financiamento**:
   - Exige entrada mínima de 20% do valor de tabela do veículo.
3. **Auditoria de Hodômetro**:
   - A quilometragem de um veículo jamais pode ser reduzida retroativamente.
4. **Ciclo de Vida do Veículo**:
   - `AVAILABLE` -> `RESERVED` -> `SOLD`. Veículo vendido não pode receber novas propostas nem ser re-vendido.
5. **Controle de Acesso (RBAC)**:
   - Ações de aprovação gerencial (`approve`) e conclusão de venda (`complete`) exigem usuário com permissão de Gerente (`IsManager`).

---

## 4. Integração com Frontend (DriveHub-Web)
- **Protocolo:** REST / JSON sobre HTTP.
- **Origem Autorizada (CORS):** `http://localhost:5173` (e portas adicionais em desenvolvimento).
- **Especificação:** OpenAPI 3 disponível em `/api/schema/` e Swagger UI em `/api/docs/`.
- **Contrato Detalhado:** Consulte `docs/CH/INTEGRACAO_CONTRATO.md`.

---

## 5. Limites e Governança
- Modificações diretas na branch `main` são estritamente proibidas.
- A integração de código depende de aprovação formal do PO.
- SQLite utilizado em desenvolvimento local; a migração para PostgreSQL com concorrência MVCC real (`SELECT ... FOR UPDATE`) é parte do backlog de infraestrutura.
- Segredos e credenciais reais nunca devem ser commitados.
