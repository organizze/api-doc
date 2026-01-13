-- =====================================================
-- SCHEMA DO DASHBOARD FINANCEIRO - SUPABASE
-- =====================================================
-- Execute este SQL no SQL Editor do Supabase

-- =====================================================
-- 1. TABELA: expected_incomes (Recebimentos Previstos)
-- =====================================================
CREATE TABLE IF NOT EXISTS expected_incomes (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),

    -- Informações do PDF/fonte
    source_document VARCHAR(255),
    client_name VARCHAR(255) NOT NULL,
    description TEXT,

    -- Valores e datas previstas
    expected_amount_cents INTEGER NOT NULL,
    expected_date DATE NOT NULL,

    -- Reconciliação com Organizze
    actual_amount_cents INTEGER DEFAULT 0,
    actual_date DATE,
    organizze_transaction_id INTEGER,

    -- Status: pending, received, partial, overdue
    status VARCHAR(20) DEFAULT 'pending',

    -- Referências do Organizze
    category_id INTEGER,
    account_id INTEGER,

    -- Período de referência
    reference_month INTEGER NOT NULL CHECK (reference_month BETWEEN 1 AND 12),
    reference_year INTEGER NOT NULL CHECK (reference_year >= 2020),

    -- Audit
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ
);

-- Índices para buscas frequentes
CREATE INDEX idx_expected_incomes_period
    ON expected_incomes(reference_year, reference_month);
CREATE INDEX idx_expected_incomes_status
    ON expected_incomes(status);
CREATE INDEX idx_expected_incomes_date
    ON expected_incomes(expected_date);

-- Trigger para atualizar updated_at
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER update_expected_incomes_updated_at
    BEFORE UPDATE ON expected_incomes
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();

-- =====================================================
-- 2. TABELA: budgets (Orçamentos/Gastos Previstos)
-- =====================================================
CREATE TABLE IF NOT EXISTS budgets (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),

    -- Categoria do Organizze
    organizze_category_id INTEGER NOT NULL,
    category_name VARCHAR(255),

    -- Período
    month INTEGER NOT NULL CHECK (month BETWEEN 1 AND 12),
    year INTEGER NOT NULL CHECK (year >= 2020),

    -- Valores
    planned_amount_cents INTEGER NOT NULL CHECK (planned_amount_cents > 0),

    -- Configuração
    is_recurring BOOLEAN DEFAULT FALSE,
    alert_threshold INTEGER DEFAULT 80 CHECK (alert_threshold BETWEEN 0 AND 100),

    -- Audit
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ,

    -- Constraint: uma categoria por mês/ano
    UNIQUE(organizze_category_id, month, year)
);

-- Índices
CREATE INDEX idx_budgets_period ON budgets(year, month);
CREATE INDEX idx_budgets_category ON budgets(organizze_category_id);

CREATE TRIGGER update_budgets_updated_at
    BEFORE UPDATE ON budgets
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();

-- =====================================================
-- 3. TABELA: investments (Investimentos)
-- =====================================================
CREATE TABLE IF NOT EXISTS investments (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),

    -- Identificação
    name VARCHAR(255) NOT NULL,
    ticker VARCHAR(20),
    -- Tipo: fixed_income, stocks, reits, crypto, savings, investment_fund, other
    type VARCHAR(50) NOT NULL,
    institution VARCHAR(255),

    -- Valores
    initial_amount_cents INTEGER NOT NULL CHECK (initial_amount_cents > 0),
    current_amount_cents INTEGER NOT NULL CHECK (current_amount_cents >= 0),

    -- Datas
    purchase_date DATE NOT NULL,
    maturity_date DATE,

    -- Rendimento
    yield_rate DECIMAL(8, 4),
    yield_type VARCHAR(50),

    -- Conta associada no Organizze
    organizze_account_id INTEGER,

    -- Notas
    notes TEXT,

    -- Status
    is_active BOOLEAN DEFAULT TRUE,

    -- Audit
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ
);

-- Índices
CREATE INDEX idx_investments_type ON investments(type);
CREATE INDEX idx_investments_active ON investments(is_active);
CREATE INDEX idx_investments_institution ON investments(institution);

CREATE TRIGGER update_investments_updated_at
    BEFORE UPDATE ON investments
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();

-- =====================================================
-- 4. TABELA: investment_history (Histórico de Investimentos)
-- =====================================================
CREATE TABLE IF NOT EXISTS investment_history (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    investment_id UUID NOT NULL REFERENCES investments(id) ON DELETE CASCADE,

    -- Snapshot
    amount_cents INTEGER NOT NULL,
    recorded_at TIMESTAMPTZ DEFAULT NOW(),

    -- Fonte: initial, manual, api, redemption
    source VARCHAR(50)
);

-- Índices
CREATE INDEX idx_investment_history_investment ON investment_history(investment_id);
CREATE INDEX idx_investment_history_date ON investment_history(recorded_at);

-- =====================================================
-- 5. POLÍTICAS DE SEGURANÇA (RLS)
-- =====================================================
-- Habilitar RLS (Row Level Security)
ALTER TABLE expected_incomes ENABLE ROW LEVEL SECURITY;
ALTER TABLE budgets ENABLE ROW LEVEL SECURITY;
ALTER TABLE investments ENABLE ROW LEVEL SECURITY;
ALTER TABLE investment_history ENABLE ROW LEVEL SECURITY;

-- Políticas para permitir todas as operações (ajuste conforme necessário)
-- Se você usar autenticação, modifique estas políticas

-- expected_incomes
CREATE POLICY "Allow all on expected_incomes" ON expected_incomes
    FOR ALL USING (true) WITH CHECK (true);

-- budgets
CREATE POLICY "Allow all on budgets" ON budgets
    FOR ALL USING (true) WITH CHECK (true);

-- investments
CREATE POLICY "Allow all on investments" ON investments
    FOR ALL USING (true) WITH CHECK (true);

-- investment_history
CREATE POLICY "Allow all on investment_history" ON investment_history
    FOR ALL USING (true) WITH CHECK (true);

-- =====================================================
-- PRONTO!
-- =====================================================
-- Após executar este script, configure seu .env com:
-- SUPABASE_URL=https://seu-projeto.supabase.co
-- SUPABASE_KEY=sua_chave_anon_ou_service_role
