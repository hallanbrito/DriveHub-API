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
    └── integration/              # Testes de Endpoints HTTP, RBAC, Transações, Hardening e Concorrência
```

---

## 💼 Regras de Negócio e Governança

- **Controle de Acesso por Perfil (RBAC)**:
  - Operações críticas como `approve` e `complete` são restritas a usuários autenticados com perfil de **Gerente** (`IsManager`).
  - Usuários anônimos e vendedores comuns são impedidos com HTTP 401/403.
- **Atomicidade e Integridade Transacional**:
  - Todas as operações compostas (ex: transição de status do veículo + registro/aprovação/conclusão de proposta) são executadas dentro de transações atômicas (`@transaction.atomic`), garantindo rollback total em caso de falha.
- **Concorrência e Persistência (SQLite vs. PostgreSQL)**:
  - A camada de repositório (`DjangoVehicleRepository` e `DjangoSaleProposalRepository`) utiliza `select_for_update()` como preparação arquitetural para produção com **PostgreSQL**.
  - **Aviso sobre SQLite em desenvolvimento**: O driver SQLite do Django ignora silenciosamente `SELECT ... FOR UPDATE`, operando sob trava de transação a nível de banco/arquivo. Desta forma, em desenvolvimento local a consistência é assegurada pela atomicidade transacional e pelas invariantes de domínio (`DomainException`). Para homologação de alta concorrência real e bloqueio a nível de linha (row-level locking via MVCC), é mandatória a adoção de PostgreSQL em ambiente de produção.
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

O sistema separa desenvolvimento local de produção via variáveis de ambiente. Em produção, a aplicação valida rigorosamente os parâmetros pré-inicialização (rejeitando `DEBUG=True`, chaves fracas ou wildcards em hosts/CORS).

Para configurar:

```bash
cp .env.example .env
```

| Variável | Descrição | Default em Dev | Comportamento em Produção |
|---|---|---|---|
| `DJANGO_ENV` | Ambiente (`development` ou `production`) | `development` | Se `production`, ativa modo estrito |
| `SECRET_KEY` | Chave secreta do Django | Chave local dev | **Obrigatória** ($\ge 32$ caracteres, sem chaves dev) |
| `DEBUG` | Modo debug | `True` | **Forçado para `False`** (rejeita se `True`) |
| `ALLOWED_HOSTS` | Hosts autorizados | `localhost,127.0.0.1` | **Obrigatório** (rejeita `*` e `0.0.0.0`) |
| `CORS_ALLOWED_ORIGINS` | Origens autorizadas para o frontend | `http://localhost:5173,...` | **Obrigatório** (rejeita `*`) |

---

## 🚀 Como Executar

### 1. Criar e Ativar Ambiente Virtual
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### 2. Aplicar Migrações e Popular Showroom (Seed Seguro)
```bash
python manage.py migrate
# Popular sem apagar dados pré-existentes:
python manage.py seed_drivehub

# Para resetar e repopular do zero em desenvolvimento:
python manage.py seed_drivehub --reset
```

> **Nota de Segurança do Seed**:
> - O comando `seed_drivehub` é **bloqueado incondicionalmente em produção** (`IS_PRODUCTION=True`).
> - Por padrão, se já existirem veículos no banco, o comando não remove nem sobrescreve dados; a limpeza exige a flag explícita `--reset`.
> - As senhas dos usuários de demonstração (`gerente` e `vendedor`) são geradas aleatoriamente via `secrets.token_urlsafe(16)` e exibidas no terminal local, podendo ser customizadas via `--manager-password` e `--seller-password`.

### 3. Iniciar Servidor
```bash
python manage.py runserver 8000
```

- **Swagger UI / Documentação Interativa**: [http://localhost:8000/api/docs/](http://localhost:8000/api/docs/)
- **OpenAPI Schema**: [http://localhost:8000/api/schema/](http://localhost:8000/api/schema/)

---

## 🧪 Testes Automatizados

Suite com **32 testes automatizados** cobrindo testes unitários, testes negativos de domínio, proteção contra concorrência, autorização RBAC, atomicidade transacional e validações de segurança em produção:

```bash
pytest -v
```
