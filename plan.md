# Plano de Implementação - Dashboard Financeiro

## Visão Geral

Dashboard financeiro integrado com a API do Organizze e Supabase, permitindo:
1. **Recebimento Previsto** - Upload de PDF com valores esperados
2. **Recebimento Atual** - Dados reais do Organizze
3. **Gastos Previstos** - Sistema de orçamento por categoria
4. **Gastos Atuais** - Despesas reais do Organizze
5. **Investimentos** - Tracking manual de investimentos

---

## Status Atual

### ✅ Implementado

| Componente | Arquivo | Status |
|------------|---------|--------|
| FastAPI App | `app/main.py` | ✅ Completo |
| Configuração | `app/config.py` | ✅ Completo |
| Conexão Supabase | `app/database.py` | ✅ Completo |
| Cliente Organizze | `app/services/organizze_client.py` | ✅ Completo |
| Parser de PDF | `app/services/pdf_parser.py` | ✅ Completo |
| Endpoints Dashboard | `app/api/v1/dashboard.py` | ✅ Completo |
| Endpoints Recebimentos | `app/api/v1/income.py` | ✅ Completo |
| Endpoints Despesas | `app/api/v1/expenses.py` | ✅ Completo |
| Endpoints Investimentos | `app/api/v1/investments.py` | ✅ Completo |
| Endpoints Organizze | `app/api/v1/organizze.py` | ✅ Completo |
| Schemas Pydantic | `app/schemas/*.py` | ✅ Completo |
| Schema SQL Supabase | `supabase_schema.sql` | ✅ Completo |

---

## Arquitetura

```
┌─────────────────────────────────────────────────────────────┐
│                        FRONTEND                              │
│                   (A implementar)                            │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                     FastAPI Backend                          │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────────────┐  │
│  │  Dashboard  │  │   Income    │  │     Expenses        │  │
│  │   /api/v1/  │  │   /api/v1/  │  │     /api/v1/        │  │
│  │  dashboard  │  │   income    │  │     expenses        │  │
│  └─────────────┘  └─────────────┘  └─────────────────────┘  │
│  ┌─────────────┐  ┌─────────────┐                           │
│  │ Investments │  │  Organizze  │                           │
│  │   /api/v1/  │  │   /api/v1/  │                           │
│  │ investments │  │  organizze  │                           │
│  └─────────────┘  └─────────────┘                           │
└─────────────────────────────────────────────────────────────┘
          │                              │
          ▼                              ▼
┌─────────────────────┐      ┌─────────────────────┐
│      Supabase       │      │    API Organizze    │
│    (PostgreSQL)     │      │  (Dados Reais)      │
│                     │      │                     │
│ • expected_incomes  │      │ • /transactions     │
│ • budgets           │      │ • /accounts         │
│ • investments       │      │ • /budgets          │
│ • investment_history│      │ • /categories       │
└─────────────────────┘      └─────────────────────┘
```

---

## Estrutura de Arquivos

```
organizzeapi/
├── app/
│   ├── __init__.py
│   ├── main.py                    # Entry point FastAPI
│   ├── config.py                  # Settings (env vars)
│   ├── database.py                # Supabase client
│   │
│   ├── api/
│   │   ├── __init__.py
│   │   └── v1/
│   │       ├── __init__.py        # Router principal
│   │       ├── dashboard.py       # GET /dashboard
│   │       ├── income.py          # Recebimentos
│   │       ├── expenses.py        # Despesas/Orçamento
│   │       ├── investments.py     # Investimentos
│   │       └── organizze.py       # Proxy Organizze
│   │
│   ├── schemas/
│   │   ├── __init__.py
│   │   ├── dashboard.py           # DashboardResponse
│   │   ├── income.py              # ExpectedIncome, ActualIncome
│   │   ├── expenses.py            # Budget, ActualExpense
│   │   └── investments.py         # Investment, InvestmentHistory
│   │
│   ├── services/
│   │   ├── __init__.py
│   │   ├── organizze_client.py    # HTTP client para Organizze
│   │   └── pdf_parser.py          # Extração de PDF
│   │
│   └── models/
│       └── __init__.py
│
├── .env.example                   # Template de configuração
├── .gitignore
├── requirements.txt               # Dependências Python
├── supabase_schema.sql           # SQL para criar tabelas
├── plan.md                        # Este arquivo
└── README.md                      # Documentação da API Organizze
```

---

## Tabelas no Supabase

### 1. expected_incomes (Recebimentos Previstos)
```sql
- id: UUID (PK)
- source_document: VARCHAR(255)     -- Nome do PDF
- client_name: VARCHAR(255)         -- Cliente/Pagador
- description: TEXT
- expected_amount_cents: INTEGER    -- Valor previsto
- expected_date: DATE               -- Data prevista
- actual_amount_cents: INTEGER      -- Valor recebido (reconciliação)
- actual_date: DATE                 -- Data real
- organizze_transaction_id: INTEGER -- ID no Organizze
- status: VARCHAR(20)               -- pending/received/partial/overdue
- reference_month: INTEGER
- reference_year: INTEGER
```

### 2. budgets (Orçamentos)
```sql
- id: UUID (PK)
- organizze_category_id: INTEGER    -- Categoria do Organizze
- category_name: VARCHAR(255)
- month: INTEGER
- year: INTEGER
- planned_amount_cents: INTEGER     -- Valor orçado
- is_recurring: BOOLEAN
- alert_threshold: INTEGER          -- % para alerta (default 80)
```

### 3. investments (Investimentos)
```sql
- id: UUID (PK)
- name: VARCHAR(255)
- ticker: VARCHAR(20)               -- Para ações/FIIs
- type: VARCHAR(50)                 -- fixed_income/stocks/reits/crypto/savings
- institution: VARCHAR(255)         -- Corretora/Banco
- initial_amount_cents: INTEGER
- current_amount_cents: INTEGER
- purchase_date: DATE
- maturity_date: DATE               -- Para renda fixa
- yield_rate: DECIMAL(8,4)
- yield_type: VARCHAR(50)           -- CDI/IPCA+/PRE
- organizze_account_id: INTEGER
- is_active: BOOLEAN
```

### 4. investment_history (Histórico)
```sql
- id: UUID (PK)
- investment_id: UUID (FK)
- amount_cents: INTEGER
- recorded_at: TIMESTAMPTZ
- source: VARCHAR(50)               -- initial/manual/redemption
```

---

## Endpoints da API

### Dashboard
| Método | Endpoint | Descrição |
|--------|----------|-----------|
| GET | `/api/v1/dashboard?month=X&year=Y` | Dashboard consolidado |

### Recebimentos (Income)
| Método | Endpoint | Descrição |
|--------|----------|-----------|
| POST | `/api/v1/income/expected/upload` | Upload PDF |
| GET | `/api/v1/income/expected` | Listar previstos |
| POST | `/api/v1/income/expected` | Criar manualmente |
| PUT | `/api/v1/income/expected/{id}` | Atualizar |
| DELETE | `/api/v1/income/expected/{id}` | Remover |
| GET | `/api/v1/income/actual` | Recebimentos do Organizze |
| GET | `/api/v1/income/comparison` | Previsto vs Realizado |
| POST | `/api/v1/income/reconcile/{expected_id}/{transaction_id}` | Reconciliar |

### Despesas (Expenses)
| Método | Endpoint | Descrição |
|--------|----------|-----------|
| GET | `/api/v1/expenses/budget` | Listar orçamentos |
| POST | `/api/v1/expenses/budget` | Criar orçamento |
| PUT | `/api/v1/expenses/budget/{id}` | Atualizar |
| DELETE | `/api/v1/expenses/budget/{id}` | Remover |
| POST | `/api/v1/expenses/budget/copy` | Copiar para próximo mês |
| GET | `/api/v1/expenses/actual` | Despesas do Organizze |
| GET | `/api/v1/expenses/by-category` | Agrupado por categoria |
| GET | `/api/v1/expenses/comparison` | Orçamento vs Realizado |

### Investimentos
| Método | Endpoint | Descrição |
|--------|----------|-----------|
| GET | `/api/v1/investments` | Listar todos |
| GET | `/api/v1/investments/summary` | Resumo consolidado |
| GET | `/api/v1/investments/{id}` | Detalhar um |
| POST | `/api/v1/investments` | Criar |
| PUT | `/api/v1/investments/{id}` | Atualizar |
| POST | `/api/v1/investments/{id}/update-value` | Atualizar valor atual |
| POST | `/api/v1/investments/{id}/redeem` | Registrar resgate |
| GET | `/api/v1/investments/{id}/history` | Histórico de valores |

### Organizze (Proxy)
| Método | Endpoint | Descrição |
|--------|----------|-----------|
| GET | `/api/v1/organizze/categories` | Categorias |
| GET | `/api/v1/organizze/accounts` | Contas bancárias |
| GET | `/api/v1/organizze/credit-cards` | Cartões de crédito |

---

## Configuração Necessária

### 1. Variáveis de Ambiente (.env)
```bash
# App
APP_NAME=FinancialDashboard
CONTACT_EMAIL=seu@email.com

# Supabase
SUPABASE_URL=https://seu-projeto.supabase.co
SUPABASE_KEY=sua_chave_anon_ou_service_role

# Organizze
ORGANIZZE_EMAIL=seu@email.com
ORGANIZZE_TOKEN=seu_token_api
```

### 2. Criar Tabelas no Supabase
Executar o conteúdo de `supabase_schema.sql` no SQL Editor do Supabase.

### 3. Obter Token do Organizze
1. Acesse https://app.organizze.com.br/configuracoes/api-keys
2. Gere um novo token
3. Copie para o `.env`

---

## Próximos Passos (Backlog)

### Prioridade Alta
- [ ] Frontend web (React/Next.js ou HTMX)
- [ ] Testes automatizados (pytest)
- [ ] Validação de erros mais robusta
- [ ] Cache de dados do Organizze (Redis)

### Prioridade Média
- [ ] Autenticação de usuários
- [ ] Multi-tenancy (múltiplos usuários)
- [ ] Notificações de alertas (email/push)
- [ ] Gráficos e visualizações
- [ ] Export de relatórios (Excel/PDF)

### Prioridade Baixa
- [ ] Integração com APIs de corretoras (CEI/B3)
- [ ] OCR para PDFs escaneados
- [ ] App mobile
- [ ] Webhooks para atualizações em tempo real

---

## Como Executar

```bash
# 1. Clonar repositório
git clone <repo-url>
cd organizzeapi

# 2. Criar ambiente virtual
python -m venv venv
source venv/bin/activate  # Linux/Mac
# ou: venv\Scripts\activate  # Windows

# 3. Instalar dependências
pip install -r requirements.txt

# 4. Configurar variáveis
cp .env.example .env
# Editar .env com suas credenciais

# 5. Criar tabelas no Supabase
# Executar supabase_schema.sql no SQL Editor

# 6. Rodar aplicação
uvicorn app.main:app --reload

# 7. Acessar documentação
# http://localhost:8000/docs
```

---

## Notas Técnicas

### API do Organizze
- Base URL: `https://api.organizze.com.br/rest/v2`
- Autenticação: HTTP Basic Auth (email + token)
- Header obrigatório: `User-Agent`
- Valores monetários em **centavos** (amount_cents)
- Receitas: `amount_cents > 0`
- Despesas: `amount_cents < 0`

### Parser de PDF
- Usa `pdfplumber` para extração de tabelas
- Suporta padrões brasileiros (R$ X.XXX,XX)
- Datas: dd/mm/yyyy ou yyyy-mm-dd
- Revisão manual recomendada após importação

### Supabase
- RLS (Row Level Security) habilitado
- Políticas permissivas por padrão (ajustar para produção)
- UUIDs como chaves primárias
- Triggers para `updated_at` automático

---

## Contato

Para dúvidas sobre este projeto, consulte a documentação da API do Organizze em `README.md` ou a documentação do FastAPI em `/docs`.
