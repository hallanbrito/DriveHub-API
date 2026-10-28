# 🚗 DriveHub API — Clean Architecture Dealership Backend

API REST corporativa para gestão comercial e governança de estoque e vendas de veículos, construída sob os princípios da **Clean Architecture** e **Domain-Driven Design (DDD)** com **Django 5** e **Django REST Framework**.

---

## 🏛️ Arquitetura do Sistema

```
DriveHub-API/
├── core/                         # Núcleo de Domínio Independente de Frameworks
│   ├── domain/
│   │   ├── entities.py           # Entidades puras (Vehicle, Brand, SaleProposal)
│   │   ├── enums.py              # Status (AVAILABLE, RESERVED, SOLD) e Pagamento
│   │   ├── exceptions.py         # Exceções de Domínio (DomainException)
│   │   └── repositories.py       # Interfaces/Protocols dos repositórios
│   └── use_cases/                # Casos de Uso (Regras de Aplicação)
│       ├── vehicles.py           # CreateVehicleUseCase, UpdateVehicleMileageUseCase
│       └── sales.py              # CreateSaleProposalUseCase, ApproveSaleProposalUseCase, CompleteSaleUseCase
│
├── apps/                         # Camada de Infraestrutura / Framework (Django & DRF)
│   ├── vehicles/                 # Models, Serializers, Views, Repositories e Seed
│   └── sales/                    # Models, Serializers, Views, Permissions e Repositories
│
├── app/                          # Configurações do Projeto Django (Settings, URLs, OpenAPI)
└── tests/                        # Pirâmide de Testes Automatizados
    ├── unit/                     # Testes de Domínio e Casos de Uso com Fakes em memória
    └── integration/              # Testes de Endpoints HTTP, RBAC, Transações e Concorrência
```

---

## 💼 Regras de Negócio e Governança

- **Controle de Acesso por Perfil (RBAC)**:
  - Operações críticas como `approve` e `complete` são restritas a usuários autenticados com perfil de **Gerente** (`IsManager`).
  - Usuários anônimos e vendedores comuns são impedidos com HTTP 401/403.
- **Atomicidade e Concorrência**:
  - Todas as operações compostas (ex: transição de status do veículo + registro/aprovação/conclusão de proposta) são executadas dentro de transações atômicas (`@transaction.atomic`).
  - Bloqueio pessimista via `select_for_update()` para impedir que múltiplos clientes reservem ou concluam venda concorrente no mesmo veículo.
- **Auditoria de Hodômetro**: A quilometragem de um veículo nunca pode ser reduzida retroativamente.
- **Validação de Anos**: O ano de fabricação deve ser $\ge 1886$ e o ano do modelo deve ser maior ou igual ao ano de fabricação.
- **Governança de Descontos**:
  - Descontos de até $5\%$: Aprovados automaticamente na alçada do vendedor.
  - Descontos entre $5{,}01\%$ e $15\%$: Exigem aprovação formal da gerência (`PENDING_MANAGER`).
  - Descontos acima de $15\%$: Vetados imediatamente pela entidade de domínio.
- **Financiamento Seguro**: Propostas na modalidade financiada exigem entrada mínima de $20\%$ do valor do veículo.
- **Ciclo de Vida da Frota**:
  - `AVAILABLE` (Disponível para propostas)
  - `RESERVED` (Reservado para o cliente que enviou proposta)
  - `SOLD` (Vendido após conclusão da proposta aprovada)

---

## ⚙️ Variáveis de Ambiente & Configuração

O sistema separa desenvolvimento local de produção via variáveis de ambiente. Para configurar:

```bash
cp .env.example .env
```

| Variável | Descrição | Default em Dev |
|---|---|---|
| `DJANGO_ENV` | Ambiente (`development` ou `production`) | `development` |
| `SECRET_KEY` | Chave secreta do Django (obrigatória em prod) | Chave local dev |
| `DEBUG` | Modo debug ativo | `True` |
| `ALLOWED_HOSTS` | Hosts autorizados separados por vírgula | `localhost,127.0.0.1` |
| `CORS_ALLOWED_ORIGINS` | Origens autorizadas para o frontend Vite | `http://localhost:5173,...` |

---

## 🚀 Como Executar

### 1. Criar e Ativar Ambiente Virtual
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### 2. Aplicar Migrações e Popular Showroom
```bash
python manage.py migrate
python manage.py seed_drivehub
```

O comando `seed_drivehub` cria automaticamente os operadores de demonstração:
- **Gerente**: usuário `gerente` | senha `gerente123` (Grupo: `Manager`, alçada de aprovação)
- **Vendedor**: usuário `vendedor` | senha `vendedor123` (Grupo: `Seller`)

### 3. Iniciar Servidor
```bash
python manage.py runserver 8000
```

- **Swagger UI / Documentação Interativa**: [http://localhost:8000/api/docs/](http://localhost:8000/api/docs/)
- **OpenAPI Schema**: [http://localhost:8000/api/schema/](http://localhost:8000/api/schema/)

---

## 🧪 Testes Automatizados

Suite com 24 testes automatizados cobrindo testes unitários, testes negativos de domínio, concorrência, autorização RBAC e atomicidade transacional:

```bash
pytest -v
```
