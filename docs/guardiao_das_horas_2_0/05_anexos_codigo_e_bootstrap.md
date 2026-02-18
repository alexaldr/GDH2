# GDH2 — Anexos: Código e Bootstrap (v1)

## Starter Kit (Poetry + Postgres)

Fonte: gdh2_starter_poetry_v2.zip

### Objetivo
Um esqueleto simples e manutenível para iniciar o repositório do Guardião das Horas 2.0, com:
- Poetry (lockfile e grupos de dependência)
- Flask (App Factory)
- SQLAlchemy 2.x + Alembic (migrations)
- PostgreSQL (Docker Compose)
- Ruff/Black/Pytest/Pre-commit

### Comandos padrão
```bash
docker compose up -d db
poetry config virtualenvs.in-project true
poetry install
cp .env.example .env
poetry run pytest
poetry run flask --app gdh2.web.app run --debug
```

### Próximo passo após bootstrap
Criar a migration `0001 extensions and enums` e aplicar:
```bash
poetry run alembic revision -m "0001 extensions and enums"
poetry run alembic upgrade head
```

---

## Alembic Revision Templates (python)

Fonte: alembic_revision_templates_gdh2.py

```python
from __future__ import annotations

"""GDH2 Alembic revision templates

These are COPY/PASTE helpers. Adjust revision/down_revision in each migration.

Design goals:
- PostgreSQL-first (tstzrange + EXCLUDE USING gist)
- Idempotency for extensions/enums
- Safe downgrade patterns
"""

from alembic import op
import sqlalchemy as sa


def create_extension_if_not_exists(ext: str) -> None:
    op.execute(sa.text(f"CREATE EXTENSION IF NOT EXISTS {ext}"))


def drop_extension_if_exists(ext: str) -> None:
    op.execute(sa.text(f"DROP EXTENSION IF EXISTS {ext}"))


def create_enum_if_not_exists(name: str, values: list[str]) -> None:
    # PostgreSQL-safe: create type only if missing
    quoted = ",".join(["'" + v.replace("'", "''") + "'" for v in values])
    op.execute(
        sa.text(
            f"""
            DO $$
            BEGIN
                IF NOT EXISTS (
                    SELECT 1 FROM pg_type t
                    JOIN pg_namespace n ON n.oid = t.typnamespace
                    WHERE t.typname = :name
                ) THEN
                    EXECUTE 'CREATE TYPE ' || quote_ident(:name) || ' AS ENUM ({quoted})';
                END IF;
            END $$;
            """.replace("{quoted}", quoted)
        ).bindparams(sa.bindparam("name", name))
    )


def drop_enum_if_exists(name: str) -> None:
    op.execute(sa.text("DO $$ BEGIN IF EXISTS (SELECT 1 FROM pg_type WHERE typname = :name) THEN EXECUTE 'DROP TYPE ' || quote_ident(:name); END IF; END $$;").bindparams(sa.bindparam("name", name)))


def create_exclusion_constraint_assignment(table: str = "assignment") -> None:
    # Example: assignment_no_overlap
    op.execute(
        sa.text(
            f"""
            ALTER TABLE {table}
              ADD CONSTRAINT assignment_no_overlap
              EXCLUDE USING gist (military_id WITH =, active_range WITH &&);
            """
        )
    )


def create_unique_index_shift_realization() -> None:
    op.execute(
        sa.text(
            """
            CREATE UNIQUE INDEX IF NOT EXISTS ux_shift_realization_one_per_plan
              ON shift_realization(schedule_item_id)
              WHERE schedule_item_id IS NOT NULL
                AND status NOT IN ('CANCELLED','REJECTED');
            """
        )
    )


def create_unique_index_ledger_idempotency() -> None:
    op.execute(
        sa.text(
            """
            CREATE UNIQUE INDEX IF NOT EXISTS ux_ledger_idempotency
              ON ledger_entry(source_type, source_id, rule_version)
              WHERE source_id IS NOT NULL;
            """
        )
    )
```
