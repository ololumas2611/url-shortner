# URL Shortener

API para encurtar URLs, redirecionar para a URL original e contar os cliques de cada link curto.

Construída com **FastAPI**, **SQLModel** e **PostgreSQL**.

## Funcionalidades

- Gerar um código curto (7 caracteres, base62) para uma URL
- Consultar a URL original a partir do código
- Redirecionar para a URL original (`302 Found`)
- Registar cada clique (data, IP, user-agent e referer)
- Contar os cliques de cada código
- Erros devolvidos sempre no mesmo formato JSON

## Estrutura

```
app/
├── main.py              # Cria a app, as tabelas e regista os handlers de erro
├── api/routes/
│   ├── urls.py          # Rotas /urls
│   └── dependecy.py     # Injeção de dependências (repositórios e services)
├── core/
│   ├── exceptions.py    # Erros da aplicação (AppError e subclasses)
│   └── error_handlers.py
├── db/database.py       # Engine e session
├── models/              # Tabelas: urls, short_codes, clicks
├── repositories/        # Acesso à base de dados
├── schemas/             # Modelos de entrada (Pydantic)
└── services/            # Regras de negócio
```

O fluxo é sempre **rota → service → repository → base de dados**.

## Como correr

### Requisitos

- Python 3.10+
- PostgreSQL

### Instalação

```bash
git clone https://github.com/ololumas2611/url-shortner.git
cd url-shortner

python3 -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate

pip install -r requirements.txt
```

### Configuração

Cria um ficheiro `.env` na raiz do projeto:

```env
DATABASE_URL=postgresql://utilizador:password@localhost:5432/url_shortener
```

> O `.env` está no `.gitignore` e não deve ser commitado.

### Arrancar

```bash
uvicorn app.main:app --reload
```

As tabelas são criadas automaticamente no arranque.

- API: http://localhost:8000
- Documentação interativa (Swagger): http://localhost:8000/docs

## Endpoints

| Método | Rota | Descrição |
|---|---|---|
| `GET` | `/health` | Verifica se a API está a funcionar |
| `POST` | `/urls/` | Cria um código curto para uma URL |
| `GET` | `/urls/{short_code}` | Devolve a URL original |
| `GET` | `/urls/{short_code}/redirect` | Redireciona para a URL original e regista o clique |
| `GET` | `/urls/{short_code}/clicks` | Devolve o total de cliques |

### Criar um código curto

```bash
curl -X POST http://localhost:8000/urls/ \
  -H "Content-Type: application/json" \
  -d '{"original_url": "https://example.com/artigo?id=42"}'
```

```json
{ "original_url": "https://example.com/artigo?id=42", "short_code": "4Ym3iva" }
```

### Consultar a URL original

```bash
curl http://localhost:8000/urls/4Ym3iva
```

```json
{ "original_url": "https://example.com/artigo?id=42", "short_code": "4Ym3iva" }
```

### Redirecionar

```bash
curl -i http://localhost:8000/urls/4Ym3iva/redirect
```

```
HTTP/1.1 302 Found
location: https://example.com/artigo?id=42
```

> No Swagger o browser segue o redirect e pode dar erro de CORS. Para testar, abre o link diretamente no browser ou usa `curl -i`.

### Contar cliques

```bash
curl http://localhost:8000/urls/4Ym3iva/clicks
```

```json
{ "short_code": "4Ym3iva", "total_clicks": 3 }
```

## Regras de negócio

### URL válida

Só uma URL válida gera um código curto. É válida quando:

- começa por `http://` ou `https://`
- tem domínio
- não tem espaços em branco

Exemplos rejeitados: `example.com`, `ftp://x.com`, `https://`, `javascript:alert(1)`.

### Geração do código

- 7 caracteres de `[a-zA-Z0-9]`, gerados com o módulo `secrets` (imprevisíveis)
- O campo `code` é `unique` na base de dados
- **Colisões:** cada tentativa de gravar o código corre dentro de um *savepoint*. Se o código já existir, desfaz-se só essa tentativa e gera-se outro (até 5 tentativas)
- A URL e o código são gravados na **mesma transação**: ou fica tudo gravado, ou nada

### Redirecionamento

Usa `302 Found` (temporário). O browser não guarda o redirect em cache, por isso cada clique passa pela API e é contado.

### Cliques

Cada redirect grava um registo em `clicks` com a data (UTC), o IP, o user-agent e o referer.
Se gravar o clique falhar, o utilizador é redirecionado na mesma: o erro vai para o log, mas o link não parte.

> Atrás de um proxy (Nginx, Docker, load balancer), o IP gravado é o do proxy. Para ter o IP real, corre o uvicorn com `--proxy-headers`.

## Erros

Todos os erros seguem o mesmo formato:

```json
{ "error": { "code": "invalid_url", "message": "URL inválida. Usa um endereço completo começado por http:// ou https://." } }
```

| Status | `code` | Quando |
|---|---|---|
| `422` | `invalid_url` | A URL não cumpre as regras |
| `404` | `short_code_not_found` | O código não existe |
| `503` | `short_code_generation_failed` | Não foi possível gerar um código único |
| `500` | `internal_error` | Erro inesperado (o detalhe fica só no log) |

Para criar um erro novo, basta uma subclasse de `AppError` em `app/core/exceptions.py`:

```python
class MeuErro(AppError):
    status_code = 400
    code = "meu_erro"
    message = "Mensagem para o utilizador."
```

## Modelo de dados

```
urls                 short_codes              clicks
─────────────        ───────────────          ─────────────────
id (PK)        ◄──── url_id (FK)              id (PK)
original_url         id (PK)           ◄───── short_code_id (FK)
created_at           code (unique)            clicked_at
                     created_at               ip
                                              user_agent
                                              referer
```

## Notas

- As tabelas são criadas com `SQLModel.metadata.create_all`, que cria tabelas novas mas **não altera** tabelas existentes. Para mudar colunas vai ser preciso migrações (ex.: Alembic).
