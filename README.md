A API do Organizze
======

Introdução
----

A API do Organizze possibilita que aplicações se comuniquem com a sua conta no sistema. Este documento explica como o Organizze funciona, quais são os objetos envolvidos e como esta comunicação pode ser feita. Esta é a primeira versão da API, ainda em versão beta, algumas mudanças e melhorias serão implementadas futuramente.


Fazendo uma requisição
----

A autenticação de todas request é via Http Basic com o Username e Password descritos abaixo:
- Username: Email da conta do Organizze
- Password: Token de acesso. Você consegue ele acessando sua conta do Organizze, no path /configuracoes/api-keys.

Todas as requisições são criptografadas, o Organizze não aceita requisições feitas com HTTP simples, apenas HTTPS. A URL base da API é https://api.organizze.com.br/rest/v2

Todas as requisições à API do Organizze devem ser acompanhadas do header User-Agent, use este header para informar qual a sua aplicação e qual o seu email para contato. Veja alguns exemplos de como você pode se identificar usando o header User-Agent:

```
User-Agent: Meu Site (falecom@admin.com.br)
User-Agent: Controle de Estoque (controledeestoque.com.br)
```

Se você não informar este header, você receberá ```400 Bad Request``` como resposta.

Apenas JSON
----

A API só suporta JSON, nós não vamos dar suporte a outro formato. Mesmo que você não utilize o header ```Content-Type: application/json; charset=utf-8``` a resposta será em JSON e com charset utf-8.

Paginação
----

Algumas requisições são paginadas, por exemplo, se você listar os contatos da sua conta, a API vai retornar os primeiros 50 contatos, para acessar a próxima página basta enviar ```&page=2``` como parâmetro. Movimentações e faturas de cartão de crédito são paginadas por período. Para informar qual período utilize os parâmetros ```&start-date=2015-09-01&end-date=2015-09-30```. Se você não informar o período o Organizze vai limitar os registros para o período atual: Mês atual para movimentações e Ano atual para faturas de cartão de crédito.

Erros
----

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
Listar usuários da conta (exclusivo versão Empresasarial do Organizze)
----

### Request:

```GET /users```

### Response:

```json
[
    {
        "id": 3,
        "name": "Esdras Mayrink",
        "email": "falecom@oesdras.com.br",
        "role": "admin"
    }
]
```

Detalhar usuário
----

### Request:

```GET /users/3```

### Response:

```json
{
    "id": 3,
    "name": "Esdras Mayrink",
    "email": "falecom@oesdras.com.br",
    "role": "admin"
}
```

Listar contas bancárias
----

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

Detalhar conta bancária
----

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

Criar conta bancária
----

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

Atualizar conta bancária
----

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

Excluir conta bancária
----

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

Listar centros de custo
----

### Request:

```GET /cost-centers```

### Response:

```json
[
    {
        "id": 1,
        "name": "Marketing",
        "parent_id": null,
        "created_at": "2015-08-31T21:28:25-03:00",
        "updated_at": "2015-08-31T21:28:25-03:00"
    },
    {
        "id": 3,
        "name": "Vendas",
        "parent_id": null,
        "created_at": "2015-08-31T21:28:25-03:00",
        "updated_at": "2015-08-31T21:28:25-03:00"
    },
    {
        "id": 4,
        "name": "Desenvolvimento",
        "parent_id": null,
        "created_at": "2015-08-31T21:29:33-03:00",
        "updated_at": "2015-08-31T21:29:33-03:00"
    },
    {
        "id": 5,
        "name": "P&D",
        "parent_id": null,
        "created_at": "2015-08-31T21:30:10-03:00",
        "updated_at": "2015-08-31T21:30:10-03:00"
    }
]
```

Detalhar conta centro de custo
----

### Request:

```GET /cost-centers/1```

### Response:

```json
{
    "id": 1,
    "name": "Marketing",
    "parent_id": null,
    "created_at": null,
    "updated_at": null
}
```

Cria um centro de custo
----

### Request:

```POST /cost-centers```

#### Body:

```json
{
    "name": "Pesquisa e Desenvolvimento"
}
```

### Response:

```json
{
    "id": 6,
    "name": "Pesquisa e Desenvolvimento",
    "parent_id": null,
    "created_at": "2015-09-15T21:20:44-03:00",
    "updated_at": "2015-09-15T21:20:44-03:00"
}
```

Atualizar um centro de custo
----

### Request:

```PUT /cost-centers/6```

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
    "parent_id": null,
    "created_at": "2015-09-15T21:20:44-03:00",
    "updated_at": "2015-09-15T21:21:43-03:00"
}
```

Excluir centro de custo
----

### Request:

```DELETE /cost-centers/6```

### Response:

```json
{
    "id": 6,
    "name": "Marketing",
    "parent_id": null,
    "created_at": "2015-09-15T21:20:44-03:00",
    "updated_at": "2015-09-15T21:21:43-03:00"
}
```

Listar categorias
----

### Request:

```GET /categories```

### Response:

```json
[
    {
        "id": 1,
        "name": "Lazer",
        "color": "438b83",
        "parent_id": null,
        "created_at": "2015-08-31T21:28:25-03:00",
        "updated_at": "2015-08-31T21:28:25-03:00"
    },
    {
        "id": 3,
        "name": "Saúde",
        "color": "ffff00",
        "parent_id": null,
        "created_at": "2015-08-31T21:28:25-03:00",
        "updated_at": "2015-08-31T21:28:25-03:00"
    },
    {
        "id": 4,
        "name": "Salário",
        "color": "66ff99",
        "parent_id": null,
        "created_at": "2015-08-31T21:29:33-03:00",
        "updated_at": "2015-08-31T21:29:33-03:00"
    },
    {
        "id": 5,
        "name": "SEO",
        "color": "cc0000",
        "parent_id": null,
        "created_at": "2015-08-31T21:30:10-03:00",
        "updated_at": "2015-08-31T21:30:10-03:00"
    }
]
```

Detalhar categoria
----

### Request:

```GET /categories/1```

### Response:

```json
{
    "id": 1,
    "name": "Lazer",
    "color": "438b83",
    "parent_id": null,
    "created_at": "2015-08-31T21:30:10-03:00",
    "updated_at": "2015-08-31T21:30:10-03:00"
}
```

Cria uma categoria
----

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
    "parent_id": null,
    "created_at": "2015-09-15T21:20:44-03:00",
    "updated_at": "2015-09-15T21:20:44-03:00"
}
```

Atualizar uma categoria
----

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
    "parent_id": null,
    "created_at": "2015-09-15T21:20:44-03:00",
    "updated_at": "2015-09-15T21:20:44-03:00"
}
```

Excluir uma categoria
----

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
    "parent_id": null,
    "created_at": "2015-09-15T21:20:44-03:00",
    "updated_at": "2015-09-15T21:20:44-03:00"
}
```


Listar cartões de crédito
----

### Request:

```GET /credit-cards```

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

Detalhar cartão de crédito
----

### Request:

```GET /credit-cards/3```

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

Criar um cartão de crédito
----

### Request:

```POST /credit-cards```

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

Atualizar um cartão de crédito
----

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

Excluir um cartão de crédito
----

### Request:

```DELETE /credit-cards/3```

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

Listar as faturas de um cartão de crédito
----

### Request:

```GET /credit-cards/3/invoices```

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

Detalhar uma fatura de cartão de crédito
----

### Request:

```GET /credit-cards/3```

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
            "payee_id": null,
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
            "payee_id": null,
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
            "payee_id": null,
            "notes": null,
            "attachments_count": 0,
            "created_at": "2015-09-01T23:42:29-03:00",
            "updated_at": "2015-09-01T23:42:29-03:00"
        }
    ]
}
```

Pagamento de uma fatura
----

### Request:

```GET /credit-cards/3/invoices/186/payments```

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
    "payee_id": null,
    "notes": "Pagamento via boleto",
    "attachments_count": 0,
    "created_at": "2015-09-15T22:27:20-03:00",
    "updated_at": "2015-09-15T22:27:20-03:00"
}
```

Listar contatos
----

### Request:

```GET /payees```

### Response:

```json
[
    {
        "id": 13,
        "name": "Someone",
        "email": "foo@bar.com",
        "phone_number": "47 3409-3099",
        "website": null,
        "notes": null,
        "created_at": "2015-09-02T13:23:40-03:00",
        "updated_at": "2015-09-02T13:45:18-03:00"
    },
    {
        "id": 14,
        "name": "Simiano",
        "email": null,
        "phone_number": "47 3409-3098",
        "website": null,
        "notes": null,
        "created_at": "2015-09-02T13:41:29-03:00",
        "updated_at": "2015-09-02T13:41:29-03:00"
    }
]
```

Detalhar um contato
----

### Request:

```GET /payees/13```

### Response:

```json
{
    "id": 1,
    "name": "Marketing",
    "parent_id": null,
    "created_at": null,
    "updated_at": null
}
```

Cria um contato
----

### Request:

```POST /payees```

#### Body:

```json
{
    "name": "João da Silva",
    "phone_number": "47 3409-3098"
}
```

### Response:

```json
{
    "id": 15,
    "name": "João da Silva",
    "email": null,
    "phone_number": "47 3409-3098",
    "website": null,
    "notes": null,
    "created_at": "2015-09-16T02:11:01-03:00",
    "updated_at": "2015-09-16T02:11:01-03:00"
}
```

Atualizar um contato
----

### Request:

```PUT /payees/14```

#### Body:

```json
{
    "phone_number": "47 3409-3000"
}
```

### Response:

```json
{
    "id": 14,
    "name": "Simiano",
    "email": null,
    "phone_number": "47 3409-3000",
    "website": null,
    "notes": null,
    "created_at": "2015-09-02T13:41:29-03:00",
    "updated_at": "2015-09-16T02:13:35-03:00"
}
```

Excluir contato
----

### Request:

```DELETE /payees/14```

### Response:

```json
{
    "id": 14,
    "name": "Simiano",
    "email": null,
    "phone_number": "47 3409-3000",
    "website": null,
    "notes": null,
    "created_at": "2015-09-02T13:41:29-03:00",
    "updated_at": "2015-09-16T02:13:35-03:00"
}
```


Listar movimentações
----

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
        "payee_id": null,
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
        "payee_id": null,
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
        "payee_id": null,
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
        "payee_id": null,
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

Detalhar uma movimentação
----

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
    "payee_id": null,
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

Cria uma movimentação
----

### Request:

```POST /transactions```

#### Body:

```json
{
    "description": "Parcelada",
    "notes": "Pagamento via boleto",
    "date": "2015-09-16",
    "recurrence_attributes": {"total": 3, "periodicity": "monthly"}
}
```

### Response:

```json
{
    "id": 97,
    "description": "Parcelada",
    "date": "2015-09-16",
    "paid": false,
    "amount_cents": 0,
    "total_installments": 1,
    "installment": 1,
    "recurring": true,
    "account_id": 3,
    "category_id": 21,
    "payee_id": null,
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

Atualizar uma movimentação
----

### Request:

```PUT /transactions/101```

#### Body:

```json
{
    "description": "Updated parcelada via API",
    "notes": "Pagamento via boleto",
    "amount_cents": 20050,
    "date": "2015-12-20",
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
    "payee_id": null,
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

Excluir movimentação
----

### Request:

```DELETE /transactions/101```

#### Body:

{
    "update_future": true
}

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
    "payee_id": null,
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

