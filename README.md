# Guardião das Horas 2.0 — Starter Kit (Poetry)

Este repositório é um esqueleto **simples e manutenível** para iniciar o GDH 2.0 com:
- Flask (App Factory)
- SQLAlchemy 2.x (sem Flask-SQLAlchemy)
- Alembic (migrations)
- Postgres (Docker Compose)
- Ruff/Black/Pytest/Pre-commit

## Requisitos
- Python 3.12+
- Poetry
- Docker + Docker Compose

## Setup rápido

1) Suba o Postgres
```bash
docker compose up -d db
```

2) Configure o Poetry para criar venv dentro do projeto (recomendado)
```bash
poetry config virtualenvs.in-project true
```

3) Instale dependências
```bash
poetry install
```

4) Crie seu .env
```bash
cp .env.example .env
```

5) Rode o servidor
```bash
poetry run flask --app gdh2.web.app run --debug
```

## Migrations (Alembic)

- Arquivos já estão em `migrations/`.
- Para criar uma revision:
```bash
poetry run alembic revision -m "0001 extensions and enums"
```
- Para aplicar:
```bash
poetry run alembic upgrade head
```

> O `alembic.ini` usa a variável `DATABASE_URL` do `.env`.

## Estrutura
- `src/gdh2/domain`: regras puras (sem Flask/DB)
- `src/gdh2/application`: casos de uso
- `src/gdh2/infra`: repositórios/integrações
- `src/gdh2/web`: rotas/serialização
- `migrations`: Alembic
