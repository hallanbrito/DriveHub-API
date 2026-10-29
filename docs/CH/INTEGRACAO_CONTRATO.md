# Contrato de Integração — Backend (DriveHub-API) & Frontend (DriveHub-Web)

> **Documento Normativo de Integração:** Define os endpoints, formatos de dados, enums, contratos de erro, requisitos de autorização e lacunas técnicas observadas entre os repositórios `DriveHub-API` e `DriveHub-Web`.

---

## 1. Visão Geral da Comunicação
- **Protocolo:** HTTP/1.1 REST sobre JSON.
- **URL Base Padrão:** `http://localhost:8000/api` (configurável no frontend via `VITE_API_URL`).
- **CORS Autorizado:** O backend aceita origens configuradas em `CORS_ALLOWED_ORIGINS` (padrão local: `http://localhost:5173`).
- **Documentação Interativa:** Swagger UI em `/api/docs/` e OpenAPI 3 Schema em `/api/schema/`.

---

## 2. Endpoints e Contratos

### 2.1. Métricas Executivas do Showroom (Summary)
- **Método & Rota:** `GET /api/vehicles/vehicles/summary/`
- **Autenticação:** Não requer autenticação (Acesso Público).
- **Resposta Sucesso (200 OK):**
```json
{
  "total_stock_value": 450000.00,
  "units_in_yard": 4,
  "open_negotiations": 2,
  "closed_revenue": 120000.00
}
```

---

### 2.2. Gestão de Veículos (Showroom)

#### Listar Veículos
- **Método & Rota:** `GET /api/vehicles/vehicles/?status={status}&search={search}`
- **Parâmetros de Consulta:**
  - `status` (opcional): `AVAILABLE`, `RESERVED`, `SOLD`. Se omitido ou `ALL`, retorna todos.
  - `search` (opcional): Busca textual por modelo, placa ou marca.
- **Resposta Sucesso (200 OK):** Lista de veículos.
```json
[
  {
    "id": 1,
    "brand_name": "Porsche",
    "model_name": "911 Carrera S",
    "factory_year": 2023,
    "model_year": 2024,
    "plate": "DRV1E23",
    "price": "890000.00",
    "mileage": 1200,
    "status": "AVAILABLE",
    "photo_url": "https://..."
  }
]
```

#### Obter Veículo por ID
- **Método & Rota:** `GET /api/vehicles/vehicles/{id}/`
- **Resposta Sucesso (200 OK):** Objeto veículo conforme acima.
- **Resposta Erro (404 Not Found):** `{"detail": "Não encontrado."}`

#### Cadastrar Veículo
- **Método & Rota:** `POST /api/vehicles/vehicles/`
- **Payload (JSON):**
```json
{
  "brand_name": "BMW",
  "model_name": "M3 Competition",
  "factory_year": 2024,
  "model_year": 2024,
  "plate": "M3C2024",
  "price": 799000.00,
  "mileage": 50,
  "photo_url": "https://..."
}
```
- **Resposta Sucesso (201 Created):** Objeto veículo criado.
- **Resposta Erro (400 Bad Request):** Violação de regras de validação ou de domínio (`{"detail": "..."}`).

#### Atualizar Hodômetro
- **Método & Rota:** `PATCH /api/vehicles/vehicles/{id}/mileage/`
- **Payload (JSON):**
```json
{
  "mileage": 1500
}
```
- **Invariante:** A quilometragem não pode ser inferior à atual.
- **Resposta Sucesso (200 OK):** Objeto veículo com quilometragem atualizada.
- **Resposta Erro (400 Bad Request):** Ex: `{"detail": "A quilometragem não pode ser reduzida."}`

---

### 2.3. Mesa de Negociações e Propostas de Venda

#### Listar Propostas
- **Método & Rota:** `GET /api/sales/proposals/?status={status}`
- **Parâmetros de Consulta:** `status` (opcional: `PENDING_MANAGER`, `APPROVED`, `REJECTED`, `COMPLETED`).
- **Resposta Sucesso (200 OK):**
```json
[
  {
    "id": 10,
    "vehicle": {
      "id": 1,
      "brand_name": "Porsche",
      "model_name": "911 Carrera S",
      "plate": "DRV1E23",
      "price": "890000.00"
    },
    "customer_name": "Carlos Silva",
    "proposed_value": "860000.00",
    "payment_method": "FINANCED",
    "down_payment": "180000.00",
    "status": "PENDING_MANAGER",
    "created_at": "2026-10-29T10:00:00Z"
  }
]
```

#### Criar Proposta de Venda
- **Método & Rota:** `POST /api/sales/proposals/`
- **Payload (JSON):**
```json
{
  "vehicle_id": 1,
  "customer_name": "Carlos Silva",
  "proposed_value": 860000.00,
  "payment_method": "FINANCED",
  "down_payment": 180000.00
}
```
- **Regras de Negócio Aplicadas no Backend:**
  - Se desconto $\le 5\%$: Proposta criada como `APPROVED`. Veículo passa para `RESERVED`.
  - Se desconto $> 5\%$ e $\le 15\%$: Proposta criada como `PENDING_MANAGER`. Veículo passa para `RESERVED`.
  - Se desconto $> 15\%$: Rejeição imediata (`400 Bad Request`).
  - Se `payment_method == "FINANCED"` e entrada $< 20\%$: Rejeição imediata (`400 Bad Request`).
- **Resposta Sucesso (201 Created):** Proposta criada.

#### Aprovar Proposta de Venda
- **Método & Rota:** `POST /api/sales/proposals/{id}/approve/`
- **Permissão Backend:** `IsManager` (Requer usuário autenticado com perfil de Gerente).
- **Resposta Sucesso (200 OK):** Proposta com status `APPROVED`.
- **Resposta Erro (401 Unauthorized / 403 Forbidden):** Usuário anônimo ou sem privilégios de gerência.

#### Concluir Venda
- **Método & Rota:** `POST /api/sales/proposals/{id}/complete/`
- **Permissão Backend:** `IsManager` (Requer usuário autenticado com perfil de Gerente).
- **Ação:** Altera o status da proposta para `COMPLETED` e o status do veículo correspondente para `SOLD` de forma atômica (`@transaction.atomic`).
- **Resposta Sucesso (200 OK):** Proposta com status `COMPLETED`.
- **Resposta Erro (401 Unauthorized / 403 Forbidden):** Falha de autorização gerencial.

---

## 3. Lacunas de Integração e Desvios Observados (Auditados na W0)

| ID | Área | Fato Observado | Impacto Funcional | Recomendação para W Posteriores |
|---|---|---|---|---|
| GAP-01 | Autenticação | `DriveHub-API` protege endpoints `approve` e `complete` com `IsManager`. `DriveHub-Web` dispara fetch anônimo sem cabeçalho `Authorization`. | Ao clicar em "Aprovar como Gerente" ou "Concluir Venda" no frontend, a chamada falha com HTTP 401/403. | Implementar módulo de autenticação (JWT / Sessão) no frontend com formulário de login e envio do token nas requisições protegidas (Alvo: W1). |
| GAP-02 | Concorrência | SQLite não possui MVCC row-level locking em desenvolvimento local. | Sob carga concorrente massiva, conflitos dependem de trava de arquivo em dev. | Migração para PostgreSQL como banco padrão em produção com MVCC ativado (Alvo: W posterior de Infra). |
| GAP-03 | Linter Web | `DriveHub-Web` apresenta 44 erros no `npm run lint` (ESLint 10), incluindo chamadas condicionais de hooks do React após early return em modais (`CreateProposalModal.jsx`, `UpdateMileageModal.jsx`). | Risco de inconsistência de estado no ciclo de renderização do React 19. | Refatoração de componentes de modais para posicionar hooks antes do early return e limpeza de variáveis não utilizadas (Alvo: W posterior de Qualidade Frontend). |
| GAP-04 | Testes Web | `DriveHub-Web` não possui suite de testes automatizados (unitários ou e2e). | Verificação do frontend restrita a build estático e linter. | Configurar Vitest + React Testing Library na esteira de qualidade do frontend (Alvo: W posterior). |
