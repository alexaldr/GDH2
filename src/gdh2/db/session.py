from __future__ import annotations

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from gdh2.settings import settings

_engine = None


def get_engine():
    global _engine
    if _engine is None:
        # Engine creation doesn't open connections; pool_pre_ping helps robustness.
        _engine = create_engine(settings.DATABASE_URL, pool_pre_ping=True)
    return _engine


# Sem bind aqui para evitar side-effects em import; o bind é aplicado no momento do uso.
SessionLocal = sessionmaker(autoflush=False, autocommit=False)


def db_session():
    """Generator de sessão com commit/rollback.

    Uso típico (ex.: em um repository):
        for db in db_session():
            ...

    Em Flask, você pode integrar isso com um teardown_request depois.
    """
    db = SessionLocal(bind=get_engine())
    try:
        yield db
        db.commit()
    except Exception:
        db.rollback()
        raise
    finally:
        db.close()
