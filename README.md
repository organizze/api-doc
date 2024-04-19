A API do Organizze
======

- [A API do Organizze](#a-api-do-organizze)
- [Introdução](#introdução)
- [Fazendo uma requisição](#fazendo-uma-requisição)
- [Apenas JSON](#apenas-json)
- [Paginação](#paginação)
- [Erros](#erros)
- [Usuários](#usuários)
- [Detalhar usuário](#detalhar-usuário)
    - [Request:](#request)
    - [Response:](#response)
- [Listar contas bancárias](#listar-contas-bancárias)
    - [Request:](#request-1)
    - [Response:](#response-1)
- [Detalhar conta bancária](#detalhar-conta-bancária)
    - [Request:](#request-2)
    - [Response:](#response-2)
- [Criar conta bancária](#criar-conta-bancária)
    - [Request:](#request-3)
      - [Body:](#body)
    - [Response:](#response-3)
- [Atualizar conta bancária](#atualizar-conta-bancária)
    - [Request:](#request-4)
      - [Body:](#body-1)
    - [Response:](#response-4)
- [Excluir conta bancária](#excluir-conta-bancária)
    - [Request:](#request-5)
    - [Response:](#response-5)
- [Listar Metas](#listar-metas)
    - [Request:](#request-6)
    - [Response:](#response-6)
- [Listar categorias](#listar-categorias)
    - [Request:](#request-7)
    - [Response:](#response-7)
- [Detalhar categoria](#detalhar-categoria)
    - [Request:](#request-8)
    - [Response:](#response-8)
- [Cria uma categoria](#cria-uma-categoria)
    - [Request](#request-9)
      - [Body:](#body-2)
    - [Response:](#response-9)
- [Atualizar uma categoria](#atualizar-uma-categoria)
    - [Request:](#request-10)
      - [Body:](#body-3)
    - [Response:](#response-10)
- [Excluir uma categoria](#excluir-uma-categoria)
    - [Request:](#request-11)
      - [Body:](#body-4)
    - [Response:](#response-11)
- [Listar cartões de crédito](#listar-cartões-de-crédito)
    - [Request:](#request-12)
    - [Response:](#response-12)
- [Detalhar cartão de crédito](#detalhar-cartão-de-crédito)
    - [Request:](#request-13)
    - [Response](#response-13)
- [Criar um cartão de crédito](#criar-um-cartão-de-crédito)
    - [Request:](#request-14)
      - [Body:](#body-5)
    - [Response:](#response-14)
- [Atualizar um cartão de crédito](#atualizar-um-cartão-de-crédito)
    - [Request:](#request-15)
      - [Body:](#body-6)
    - [Response:](#response-15)
- [Excluir um cartão de crédito](#excluir-um-cartão-de-crédito)
    - [Request:](#request-16)
    - [Response:](#response-16)
- [Listar as faturas de um cartão de crédito](#listar-as-faturas-de-um-cartão-de-crédito)
    - [Request:](#request-17)
    - [Response:](#response-17)
- [Detalhar uma fatura de cartão de crédito](#detalhar-uma-fatura-de-cartão-de-crédito)
    - [Request:](#request-18)
    - [Response:](#response-18)
- [Pagamento de uma fatura](#pagamento-de-uma-fatura)
    - [Request:](#request-19)
    - [Response:](#response-19)
- [Listar movimentações](#listar-movimentações)
    - [Filtros:](#filtros)
    - [Request:](#request-20)
    - [Response:](#response-20)
- [Detalhar uma movimentação](#detalhar-uma-movimentação)
    - [Request:](#request-21)
    - [Response:](#response-21)
- [Cria uma movimentação.](#cria-uma-movimentação)
    - [Request:](#request-22)
      - [Body:](#body-7)
    - [Response:](#response-22)
- [Cria uma movimentação recorrente (fixa).](#cria-uma-movimentação-recorrente-fixa)
    - [Request:](#request-23)
      - [Body:](#body-8)
    - [Response:](#response-23)
- [Cria uma movimentação recorrente (parcelada).](#cria-uma-movimentação-recorrente-parcelada)
    - [Request:](#request-24)
      - [Body:](#body-9)
    - [Response:](#response-24)
- [Atualizar uma movimentação](#atualizar-uma-movimentação)
    - [Request:](#request-25)
      - [Body:](#body-10)
    - [Response:](#response-25)
- [Excluir movimentação](#excluir-movimentação)
    - [Request:](#request-26)
      - [Body:](#body-11)
    - [Response:](#response-26)

# Introdução

A API do Organizze possibilita que aplicações se comuniquem com a sua conta no sistema. Este documento explica como o Organizze funciona, quais são os objetos envolvidos e como esta comunicação pode ser feita. Esta é a primeira versão da API, ainda em versão beta, algumas mudanças e melhorias serão implementadas futuramente.

# OpenAPI
Você também pode acessar a documentação OpenAPI da API do Organizze em formato JSON. [Documentação OpenAPI](./api/openapi.json). Essa documentação contém apenas algumas requisições GET, que são usadas através do ChatGPT.

# Fazendo uma requisição

A autenticação de todas request é via Http Basic com o Username e Password descritos abaixo:
- Username: Email da conta do Organizze
- Password: Token de acesso. Você consegue ele acessando sua conta do Organizze, na url https://app.organizze.com.br/configuracoes/api-keys.

Todas as requisições são criptografadas, o Organizze não aceita requisições feitas com HTTP simples, apenas HTTPS. A URL base da API é https://api.organizze.com.br/rest/v2

Todas as requisições à API do Organizze devem ser acompanhadas do header User-Agent, use este header para informar qual a sua aplicação e qual o seu email para contato. Veja alguns exemplos de como você pode se identificar usando o header User-Agent:

```
User-Agent: Esdras (esdras@organizze.com.br)
User-Agent: Alex (alex@gmail.com)
```

Se você não informar este header, você receberá ```400 Bad Request``` como resposta.

# Apenas JSON

A API só suporta JSON, nós não vamos dar suporte a outro formato. Mesmo que você não utilize o header ```Content-Type: application/json; charset=utf-8``` a resposta será em JSON e com charset utf-8.

# Paginação

Movimentações e faturas de cartão de crédito são paginadas por período. Para informar qual período utilize os parâmetros ```&start_date=2015-09-01&end_date=2015-09-30```. Se você não informar o período o Organizze vai limitar os registros para o período atual: Mês atual para movimentações e Ano atual para faturas de cartão de crédito.

# Erros

Abaixo estão listados alguns exemplos de erros que podem acontecer e as suas respectivas respostas:

Autorização negada: O email ou senha estão incorretos ou o usuário não está autenticado, o status HTTP é 401 e o body é:

```json
{
    "error": "Não autorizado"
}
```

Uma tentativa de criar ou atualizar um registro inválido. No exemplo abaixo o usuário está tentando criar uma conta bancária sem nome, o status HTTP é 422 e o body é:

```json
{
    "id": null,
    "name": null,
    "description": "Minha conta corrente",
    "archived": false,
    "created_at": null,
    "updated_at": null,
    "default": false,
    "errors": {
        "name": [
            "não pode estar em branco"
        ]
    },
    "type": "checking"
}
```

Usuários
====
# Detalhar usuário

### Request:

```GET /users/3```

### Response:

```json
{
    "id": 3,
    "name": "Esdras Mayrink",
    "email": "falecom@email.com.br",
    "role": "admin"
}
```

# Listar contas bancárias

### Request:

```GET /accounts```

### Response:

```json
[
    {
        "id": 3,
        "name": "Bradesco CC",
        "description": "Some descriptions",
        "archived": false,
        "created_at": "2015-06-22T16:17:03-03:00",
        "updated_at": "2015-08-31T22:24:24-03:00",
        "default": true,
        "type": "checking"
    },
    {
        "id": 4,
        "name": "Caixa Poupança",
        "description": "",
        "archived": false,
        "created_at": "2015-08-20T17:59:06-03:00",
        "updated_at": "2015-08-31T18:46:23-03:00",
        "default": false,
        "type": "savings"
    },
    {
        "id": 5,
        "name": "Carteira",
        "description": null,
        "archived": false,
        "created_at": "2015-08-31T18:19:01-03:00",
        "updated_at": "2015-08-31T18:19:01-03:00",
        "default": false,
        "type": "other"
    }
]
```

# Detalhar conta bancária

### Request:

```GET /accounts/3```

### Response:

```json
{
    "id": 3,
    "name": "Bradesco CC",
    "description": "Some descriptions",
    "archived": false,
    "created_at": "2015-06-22T16:17:03-03:00",
    "updated_at": "2015-08-31T22:24:24-03:00",
    "default": true,
    "type": "checking"
}
```

# Criar conta bancária

### Request:

```POST /accounts```

#### Body:

```json
{
    "name": "Itaú CC",
    "type": "checking",
    "description": "Minha conta corrente",
    "default": true
}
```

### Response:

```json
{
    "id": 18,
    "name": "Itaú CC",
    "description": "Minha conta corrente",
    "archived": false,
    "created_at": "2015-09-15T21:04:30-03:00",
    "updated_at": "2015-09-15T21:04:30-03:00",
    "default": true,
    "type": "checking"
}
```

# Atualizar conta bancária

### Request:

```PUT /accounts/18```

#### Body:

```json
{
    "name": "Itaú Poupança",
}
```

### Response:

```json
{
    "id": 18,
    "name": "Itaú Poupança",
    "description": "Minha conta corrente",
    "archived": false,
    "created_at": "2015-09-15T21:04:30-03:00",
    "updated_at": "2015-09-15T21:04:30-03:00",
    "default": true,
    "type": "checking"
}
```

# Excluir conta bancária

### Request:

```DELETE /accounts/18```

### Response:

```json
{
    "id": 18,
    "name": "Itaú Poupança",
    "description": "Minha conta corrente",
    "archived": false,
    "created_at": "2015-09-15T21:04:30-03:00",
    "updated_at": "2015-09-15T21:04:30-03:00",
    "default": true,
    "type": "checking"
}
```

# Listar Metas

Ao chamar a raiz desse endpoint, ira receber todas as metas referentes ao mês atual.

Para retornar todas as metas referentes ao ano, basta escopar na url ```/budgets/2018```

Metas referentes ao mês e ano, basta escopar na url ```/budgets/2018/08``` 


### Request:

```GET /budgets```

### Response:

```json
[
    {
        "amount_in_cents": 150000,
        "category_id": 17,
        "date": "2018-08-01",
        "activity_type": 0,
        "total": 0,
        "predicted_total": 0,
        "percentage": "0.0"
    },
    {
        "amount_in_cents": 30000,
        "category_id": 13,
        "date": "2018-08-01",
        "activity_type": 0,
        "total": 0,
        "predicted_total": 0,
        "percentage": "0.0"
    }
]
```

# Listar categorias

### Request:

```GET /categories```

### Response:

```json
[
    {
        "id": 1,
        "name": "Lazer",
        "color": "438b83",
        "parent_id": null
    },
    {
        "id": 3,
        "name": "Saúde",
        "color": "ffff00",
        "parent_id": null
    },
    {
        "id": 4,
        "name": "Salário",
        "color": "66ff99",
        "parent_id": null
    },
    {
        "id": 5,
        "name": "SEO",
        "color": "cc0000",
        "parent_id": null
    }
]
```

# Detalhar categoria

### Request:

```GET /categories/1```

### Response:

```json
{
    "id": 1,
    "name": "Lazer",
    "color": "438b83",
    "parent_id": null
}
```

# Cria uma categoria

### Request

```POST /categories```

#### Body:

```json
{
    "name": "SEO"
}
```

### Response:

```json
{
    "id": 6,
    "name": "SEO",
    "color": "8dd47f",
    "parent_id": null
}
```

# Atualizar uma categoria

### Request:

```PUT /categories/6```

#### Body:

```json
{
    "name": "Marketing",
}
```

### Response:

```json
{
    "id": 6,
    "name": "Marketing",
    "color": "8dd47f",
    "parent_id": null
}
```

# Excluir uma categoria

Ao excluir uma categoria você pode informar uma categoria para substitui-la, todas as movimentações da categoria excluídas serão transferidas para a categoria substituta. Se a categoria substituta não for informada, a categoria padrão substituirá a categoria excluída.

### Request:

```DELETE /categories/6```

#### Body:

```json
{
    "replacement_id": 18
}
```

### Response:

```json
{
    "id": 6,
    "name": "Marketing",
    "color": "8dd47f",
    "parent_id": null
}
```


# Listar cartões de crédito

### Request:

```GET /credit_cards```

### Response:

```json
[
    {
        "id": 3,
        "name": "Visa Exclusive",
        "description": null,
        "card_network": "visa",
        "closing_day": 4,
        "due_day": 17,
        "limit_cents": 1200000,
        "kind": "credit_card",
        "archived": true,
        "default": false,
        "created_at": "2015-06-22T16:45:30-03:00",
        "updated_at": "2015-09-01T18:18:48-03:00"
    },
    {
        "id": 4,
        "name": "Sem limite",
        "description": null,
        "card_network": null,
        "closing_day": 2,
        "due_day": 15,
        "limit_cents": 0,
        "kind": "credit_card",
        "archived": false,
        "default": false,
        "created_at": "2015-09-01T18:06:16-03:00",
        "updated_at": "2015-09-01T18:06:16-03:00"
    }
]
```

# Detalhar cartão de crédito

### Request:

```GET /credit_cards/3```

### Response

```json
{
    "id": 3,
    "name": "Visa Exclusive",
    "description": null,
    "card_network": "visa",
    "closing_day": 4,
    "due_day": 17,
    "limit_cents": 1200000,
    "kind": "credit_card",
    "archived": true,
    "default": false,
    "created_at": "2015-06-22T16:45:30-03:00",
    "updated_at": "2015-09-01T18:18:48-03:00"
}
```

# Criar um cartão de crédito

### Request:

```POST /credit_cards```

#### Body:

```json
{
    "name": "Hipercard",
    "card_network": "hipercard",
    "due_day": 15,
    "closing_day": 2,
    "limit_cents": 500000
}
```

### Response:

```json
{
    "id": 6,
    "name": "Hipercard",
    "description": null,
    "card_network": "hipercard",
    "closing_day": 2,
    "due_day": 15,
    "limit_cents": 500000,
    "kind": "credit_card",
    "archived": false,
    "default": false,
    "created_at": "2015-09-15T22:02:55-03:00",
    "updated_at": "2015-09-15T22:02:55-03:00"
}
```

# Atualizar um cartão de crédito

### Request:

```PUT /categories/6```

#### Body:

```json
{
    "name": "Visa Exclusive",
    "due_day": 17,
    "closing_day": 4,
    "update_invoices_since": "2015-07-01"
}
```

### Response:

```json
{
    "id": 3,
    "name": "Visa Exclusive",
    "description": null,
    "card_network": "visa",
    "closing_day": 4,
    "due_day": 17,
    "limit_cents": 1200000,
    "kind": "credit_card",
    "archived": true,
    "default": false,
    "created_at": "2015-06-22T16:45:30-03:00",
    "updated_at": "2015-09-01T18:18:48-03:00"
}
```

# Excluir um cartão de crédito

### Request:

```DELETE /credit_cards/3```

### Response:

```json
{
    "id": 3,
    "name": "Visa Exclusive",
    "description": null,
    "card_network": "visa",
    "closing_day": 4,
    "due_day": 17,
    "limit_cents": 1200000,
    "kind": "credit_card",
    "archived": true,
    "default": false,
    "created_at": "2015-06-22T16:45:30-03:00",
    "updated_at": "2015-09-01T18:18:48-03:00"
}
```

# Listar as faturas de um cartão de crédito

### Request:

```GET /credit_cards/3/invoices```

### Response:

```json
[
    {
        "id": 180,
        "date": "2015-01-15",
        "starting_date": "2014-12-03",
        "closing_date": "2015-01-02",
        "amount_cents": 0,
        "payment_amount_cents": 0,
        "balance_cents": 0,
        "previous_balance_cents": 0,
        "credit_card_id": 3
    },
    {
        "id": 181,
        "date": "2015-02-15",
        "starting_date": "2015-01-03",
        "closing_date": "2015-02-02",
        "amount_cents": 0,
        "payment_amount_cents": 0,
        "balance_cents": 0,
        "previous_balance_cents": 0,
        "credit_card_id": 3
    },
    {
        "id": 182,
        "date": "2015-03-15",
        "starting_date": "2015-02-03",
        "closing_date": "2015-03-02",
        "amount_cents": 0,
        "payment_amount_cents": 0,
        "balance_cents": 0,
        "previous_balance_cents": 0,
        "credit_card_id": 3
    },
    {
        "id": 183,
        "date": "2015-04-15",
        "starting_date": "2015-03-03",
        "closing_date": "2015-04-02",
        "amount_cents": 0,
        "payment_amount_cents": 0,
        "balance_cents": 0,
        "previous_balance_cents": 0,
        "credit_card_id": 3
    },
    {
        "id": 184,
        "date": "2015-05-15",
        "starting_date": "2015-04-03",
        "closing_date": "2015-05-02",
        "amount_cents": -25098,
        "payment_amount_cents": 0,
        "balance_cents": -25098,
        "previous_balance_cents": 0,
        "credit_card_id": 3
    },
    {
        "id": 185,
        "date": "2015-06-15",
        "starting_date": "2015-05-03",
        "closing_date": "2015-06-02",
        "amount_cents": 584900,
        "payment_amount_cents": 0,
        "balance_cents": 584900,
        "previous_balance_cents": 0,
        "credit_card_id": 3
    },
    {
        "id": 186,
        "date": "2015-07-17",
        "starting_date": "2015-06-03",
        "closing_date": "2015-07-04",
        "amount_cents": 30000,
        "payment_amount_cents": -70000,
        "balance_cents": 100000,
        "previous_balance_cents": 0,
        "credit_card_id": 3
    },
    {
        "id": 187,
        "date": "2015-08-17",
        "starting_date": "2015-07-05",
        "closing_date": "2015-08-04",
        "amount_cents": -22098,
        "payment_amount_cents": 0,
        "balance_cents": 77902,
        "previous_balance_cents": 100000,
        "credit_card_id": 3
    },
    {
        "id": 188,
        "date": "2015-09-17",
        "starting_date": "2015-08-05",
        "closing_date": "2015-09-04",
        "amount_cents": -15000,
        "payment_amount_cents": 0,
        "balance_cents": -15000,
        "previous_balance_cents": 0,
        "credit_card_id": 3
    },
    {
        "id": 189,
        "date": "2015-10-17",
        "starting_date": "2015-09-05",
        "closing_date": "2015-10-04",
        "amount_cents": -15000,
        "payment_amount_cents": 0,
        "balance_cents": -15000,
        "previous_balance_cents": 0,
        "credit_card_id": 3
    },
    {
        "id": 190,
        "date": "2015-11-17",
        "starting_date": "2015-10-05",
        "closing_date": "2015-11-04",
        "amount_cents": -30000,
        "payment_amount_cents": 0,
        "balance_cents": -30000,
        "previous_balance_cents": 0,
        "credit_card_id": 3
    },
    {
        "id": 191,
        "date": "2015-12-17",
        "starting_date": "2015-11-05",
        "closing_date": "2015-12-04",
        "amount_cents": -15000,
        "payment_amount_cents": 0,
        "balance_cents": -15000,
        "previous_balance_cents": 0,
        "credit_card_id": 3
    }
]
```

# Detalhar uma fatura de cartão de crédito

### Request:

```GET /credit_cards/3/invoices/186```

### Response:

```json
{
    "id": 186,
    "date": "2015-07-17",
    "starting_date": "2015-06-03",
    "closing_date": "2015-07-04",
    "amount_cents": 30000,
    "payment_amount_cents": -70000,
    "balance_cents": 100000,
    "previous_balance_cents": 0,
    "credit_card_id": 3,
    "transactions": [
        {
            "id": 19,
            "description": "Gasto no cartão",
            "date": "2015-06-03",
            "paid": true,
            "amount_cents": -5000,
            "total_installments": 1,
            "installment": 1,
            "recurring": false,
            "account_id": 3,
            "account_type": "CreditCard",
            "category_id": 21,
            "contact_id": null,
            "notes": "",
            "attachments_count": 0,
            "created_at": "2015-08-04T20:13:49-03:00",
            "updated_at": "2015-08-04T20:14:04-03:00"
        },
        {
            "id": 12,
            "description": "SAQUE LOT",
            "date": "2015-06-06",
            "paid": true,
            "amount_cents": -15000,
            "total_installments": 5,
            "installment": 1,
            "recurring": false,
            "account_id": 3,
            "account_type": "CreditCard",
            "category_id": 21,
            "contact_id": null,
            "notes": "",
            "attachments_count": 0,
            "created_at": "2015-07-01T10:52:06-03:00",
            "updated_at": "2015-08-04T20:17:17-03:00"
        }
    ],
    "payments": [
        {
            "id": 83,
            "description": "Pagamento Julho de 2015",
            "date": "2015-09-01",
            "paid": true,
            "amount_cents": -20000,
            "total_installments": 1,
            "installment": 1,
            "recurring": false,
            "account_id": 3,
            "account_type": "Account",
            "category_id": 21,
            "contact_id": null,
            "notes": null,
            "attachments_count": 0,
            "created_at": "2015-09-01T23:42:29-03:00",
            "updated_at": "2015-09-01T23:42:29-03:00"
        }
    ]
}
```

# Pagamento de uma fatura

### Request:

```GET /credit_cards/3/invoices/186/payments```

### Response:

```json
{
    "id": 1033,
    "description": "Pagamento fatura",
    "date": "2015-09-16",
    "paid": true,
    "amount_cents": 0,
    "total_installments": 1,
    "installment": 1,
    "recurring": false,
    "account_id": 3,
    "account_type": "Account",
    "category_id": 21,
    "contact_id": null,
    "notes": "Pagamento via boleto",
    "attachments_count": 0,
    "created_at": "2015-09-15T22:27:20-03:00",
    "updated_at": "2015-09-15T22:27:20-03:00"
}
```

# Listar movimentações
A paginação de movimentações é feita com os parâmetros start_date e end_date, conforme descrito na seção de Paginação acima. O periodo processado será sempre mês inteiro. Ou seja, seu start_date é sempre processado como ```start_date.beginning_of_month``` e o seu end_date é sempre convertido para ```end_date.end_of_month```.

### Filtros:
Esse endpoint permite filtrar por uma conta bancária (account_id).
Para isso, deve enviar o parâmetro ```account_id``` com o id da conta bancária que deseja filtrar.

**No endpoint de contas bancárias ```/accounts```, é possível obter o id de todas suas contas bancárias. 

### Request:

```GET /transactions```

### Response:

```json
[
    {
        "id": 15,
        "description": "SAQUE LOT",
        "date": "2015-09-06",
        "paid": false,
        "amount_cents": -15000,
        "total_installments": 1,
        "installment": 1,
        "recurring": false,
        "account_id": 3,
        "account_type": "CreditCard",
        "category_id": 21,
        "contact_id": null,
        "notes": "",
        "attachments_count": 0,
        "credit_card_id": 3,
        "credit_card_invoice_id": 189,
        "paid_credit_card_id": null,
        "paid_credit_card_invoice_id": null,
        "oposite_transaction_id": null,
        "oposite_account_id": null,
        "created_at": "2015-07-01T10:52:06-03:00",
        "updated_at": "2015-08-04T20:17:17-03:00"
    },
    {
        "id": 31,
        "description": "Lanche",
        "date": "2015-09-02",
        "paid": false,
        "amount_cents": -2098,
        "total_installments": 1,
        "installment": 1,
        "recurring": false,
        "account_id": 3,
        "account_type": "Account",
        "category_id": 18,
        "contact_id": null,
        "notes": "",
        "attachments_count": 0,
        "credit_card_id": null,
        "credit_card_invoice_id": null,
        "paid_credit_card_id": null,
        "paid_credit_card_invoice_id": null,
        "oposite_transaction_id": 63,
        "oposite_account_id": 4,
        "created_at": "2015-08-20T18:00:20-03:00",
        "updated_at": "2015-09-01T18:14:54-03:00"
    },
    {
        "id": 63,
        "description": "Gasolina",
        "date": "2015-09-02",
        "paid": false,
        "amount_cents": 20000,
        "total_installments": 1,
        "installment": 1,
        "recurring": false,
        "account_id": 4,
        "account_type": "Account",
        "category_id": 18,
        "contact_id": null,
        "notes": "",
        "attachments_count": 0,
        "credit_card_id": null,
        "credit_card_invoice_id": null,
        "paid_credit_card_id": null,
        "paid_credit_card_invoice_id": null,
        "oposite_transaction_id": 31,
        "oposite_account_id": 3,
        "created_at": "2015-08-20T18:00:20-03:00",
        "updated_at": "2015-09-01T18:14:54-03:00"
    },
    {
        "id": 83,
        "description": "Pagamento Julho de 2015",
        "date": "2015-09-01",
        "paid": true,
        "amount_cents": -20000,
        "total_installments": 1,
        "installment": 1,
        "recurring": false,
        "account_id": 3,
        "account_type": "Account",
        "category_id": 21,
        "contact_id": null,
        "notes": null,
        "attachments_count": 0,
        "credit_card_id": null,
        "credit_card_invoice_id": null,
        "paid_credit_card_id": 3,
        "paid_credit_card_invoice_id": 186,
        "oposite_transaction_id": null,
        "oposite_account_id": null,
        "created_at": "2015-09-01T23:42:29-03:00",
        "updated_at": "2015-09-01T23:42:29-03:00"
    }
]
```

# Detalhar uma movimentação

### Request:

```GET /transactions/15```

### Response:

```json
{
    "id": 15,
    "description": "SAQUE LOT",
    "date": "2015-09-06",
    "paid": false,
    "amount_cents": -15000,
    "total_installments": 1,
    "installment": 1,
    "recurring": false,
    "account_id": 3,
    "category_id": 21,
    "contact_id": null,
    "notes": "",
    "attachments_count": 0,
    "credit_card_id": 3,
    "credit_card_invoice_id": 189,
    "paid_credit_card_id": null,
    "paid_credit_card_invoice_id": null,
    "oposite_transaction_id": null,
    "oposite_account_id": null,
    "created_at": "2015-07-01T10:52:06-03:00",
    "updated_at": "2015-08-04T20:17:17-03:00"
}
```

# Cria uma movimentação.

### Request:

```POST /transactions```

#### Body:

```json
{
    "description": "Computador",
    "notes": "Pagamento via boleto",
    "date": "2015-09-16",
    "tags": [{"name": "homeoffice"}]
}
```

### Response:

```json
{
    "id": 97,
    "description": "Computador",
    "date": "2015-09-16",
    "paid": false,
    "amount_cents": 0,
    "total_installments": 1,
    "installment": 1,
    "recurring": false,
    "account_id": 3,
    "category_id": 21,
    "contact_id": null,
    "notes": "Pagamento via boleto",
    "attachments_count": 0,
    "credit_card_id": null,
    "credit_card_invoice_id": null,
    "paid_credit_card_id": null,
    "paid_credit_card_invoice_id": null,
    "oposite_transaction_id": null,
    "oposite_account_id": null,
    "created_at": "2015-09-04T00:09:34-03:00",
    "updated_at": "2015-09-04T00:09:34-03:00",
    "tags": [{"name": "homeoffice"}]
}
```


# Cria uma movimentação recorrente (fixa).

Os valores para `periodicity` são: `["monthly", "yearly", "weekly", "biweekly", "bimonthly", "trimonthly"]`

### Request:

```POST /transactions```

#### Body:

```json
{
    "description": "Despesa fixa",
    "notes": "Pagamento via boleto",
    "date": "2015-09-16",
    "recurrence_attributes": {"periodicity": "monthly"}
}
```

### Response:

```json
{
    "id": 97,
    "description": "Despesa fixa",
    "date": "2015-09-16",
    "paid": false,
    "amount_cents": 0,
    "total_installments": 1,
    "installment": 1,
    "recurring": true,
    "account_id": 3,
    "category_id": 21,
    "contact_id": null,
    "notes": "Pagamento via boleto",
    "attachments_count": 0,
    "credit_card_id": null,
    "credit_card_invoice_id": null,
    "paid_credit_card_id": null,
    "paid_credit_card_invoice_id": null,
    "oposite_transaction_id": null,
    "oposite_account_id": null,
    "created_at": "2015-09-04T00:09:34-03:00",
    "updated_at": "2015-09-04T00:09:34-03:00"
}
```




# Cria uma movimentação recorrente (parcelada).

Os valores para `periodicity` são: `["monthly", "yearly", "weekly", "biweekly", "bimonthly", "trimonthly"]`

### Request:

```POST /transactions```

#### Body:

```json
{
    "description": "Despesa parcelada",
    "notes": "Pagamento via boleto",
    "date": "2015-09-16",
    "installments_attributes": {"periodicity": "monthly", "total": 12}
}
```

### Response:

```json
{
    "id": 97,
    "description": "Despesa parcelada",
    "date": "2015-09-16",
    "paid": false,
    "amount_cents": 0,
    "total_installments": 12,
    "installment": 1,
    "recurring": false,
    "account_id": 3,
    "category_id": 21,
    "contact_id": null,
    "notes": "Pagamento via boleto",
    "attachments_count": 0,
    "credit_card_id": null,
    "credit_card_invoice_id": null,
    "paid_credit_card_id": null,
    "paid_credit_card_invoice_id": null,
    "oposite_transaction_id": null,
    "oposite_account_id": null,
    "created_at": "2015-09-04T00:09:34-03:00",
    "updated_at": "2015-09-04T00:09:34-03:00"
}
```


# Atualizar uma movimentação

No caso de movimentações fixas ou parceladas, para atualizar a movimentação e as próximas ocorrências envie o attributo `"update_future": true`; Caso queira atualizar todas as ocorrências, inclusive as anteriores, envie o attributo `"update_all": true`. Observe que este último pode alterar o saldo da conta caso as movimentações anteriores já estejam pagas/recebidas.

### Request:

```PUT /transactions/101```

#### Body:

```json
{
    "description": "Updated parcelada via API",
    "notes": "Pagamento via boleto",
    "amount_cents": 20050,
    "date": "2015-12-20",
    "update_future": true,
    "tags": [{"name": "via_api"}]
}
```

### Response:

```json
{
    "id": 101,
    "description": "Updated parcelada via API",
    "date": "2015-12-20",
    "paid": false,
    "amount_cents": -20050,
    "total_installments": 1,
    "installment": 1,
    "recurring": true,
    "account_id": 3,
    "category_id": 21,
    "contact_id": null,
    "notes": "Pagamento via boleto",
    "attachments_count": 0,
    "credit_card_id": null,
    "credit_card_invoice_id": null,
    "paid_credit_card_id": null,
    "paid_credit_card_invoice_id": null,
    "oposite_transaction_id": null,
    "oposite_account_id": null,
    "created_at": "2015-09-04T00:09:34-03:00",
    "updated_at": "2015-09-04T00:34:54-03:00",
    "tags": [{"name": "via_api"}]
}
```

# Excluir movimentação

No caso de movimentações fixas ou parceladas, para excluir a movimentação e as próximas ocorrências envie o attributo `"update_future": true`; Caso queira excluir todas as ocorrências, inclusive as anteriores, envie o attributo `"update_all": true`. Observe que este último pode alterar o saldo da conta caso as movimentações anteriores já estejam pagas/recebidas.

### Request:

```DELETE /transactions/101```


#### Body:

```json
{
    "update_future": true
}
```

### Response:

```json
{
    "id": 101,
    "description": "Updated parcelada via API",
    "date": "2015-12-20",
    "paid": false,
    "amount_cents": -20050,
    "total_installments": 1,
    "installment": 1,
    "recurring": true,
    "account_id": 3,
    "category_id": 21,
    "contact_id": null,
    "notes": "Pagamento via boleto",
    "attachments_count": 0,
    "credit_card_id": null,
    "credit_card_invoice_id": null,
    "paid_credit_card_id": null,
    "paid_credit_card_invoice_id": null,
    "oposite_transaction_id": null,
    "oposite_account_id": null,
    "created_at": "2015-09-04T00:09:34-03:00",
    "updated_at": "2015-09-04T00:34:54-03:00"
}
```
