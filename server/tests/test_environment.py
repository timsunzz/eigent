from app.component.environment import env, normalize_database_url


def test_env_reads_uppercase_alias(monkeypatch):
    monkeypatch.delenv("database_url", raising=False)
    monkeypatch.setenv("DATABASE_URL", "postgresql://example")
    assert env("database_url") == "postgresql://example"


def test_env_reads_secret_key_alias(monkeypatch):
    monkeypatch.delenv("secret_key", raising=False)
    monkeypatch.setenv("SECRET_KEY", "from-host")
    assert env("secret_key") == "from-host"


def test_normalize_database_url_rewrites_postgres_scheme():
    assert (
        normalize_database_url("postgres://user:pass@host/db")
        == "postgresql://user:pass@host/db"
    )
    assert (
        normalize_database_url("postgresql://user:pass@host/db")
        == "postgresql://user:pass@host/db"
    )
