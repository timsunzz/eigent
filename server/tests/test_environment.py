from app.component.database import normalize_database_url
from app.component.environment import env


def test_env_reads_uppercase_alias(monkeypatch):
    monkeypatch.delenv("database_url", raising=False)
    monkeypatch.setenv("DATABASE_URL", "postgresql://example")
    assert env("database_url") == "postgresql://example"


def test_normalize_database_url_rewrites_postgres_scheme():
    assert (
        normalize_database_url("postgres://user:pass@host/db")
        == "postgresql://user:pass@host/db"
    )
    assert (
        normalize_database_url("postgresql://user:pass@host/db")
        == "postgresql://user:pass@host/db"
    )
