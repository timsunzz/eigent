from app.component.environment import env, normalize_database_url, router_prefixes


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


def test_router_prefixes_always_include_root_and_api():
    assert router_prefixes("") == ["", "/api"]
    assert router_prefixes(None) == ["", "/api"]
    assert router_prefixes("/api") == ["/api", ""]
    assert router_prefixes("/v1") == ["/v1", "", "/api"]


def test_auto_include_routers_mounts_multiple_prefixes(tmp_path):
    from fastapi import FastAPI
    from fastapi.testclient import TestClient

    from app.component.environment import auto_include_routers

    (tmp_path / "ping_controller.py").write_text(
        "from fastapi import APIRouter\n"
        "router = APIRouter()\n"
        "@router.get('/ping')\n"
        "def ping():\n"
        "    return {'ok': True}\n"
    )
    app = FastAPI()
    auto_include_routers(app, ["", "/api"], str(tmp_path))
    client = TestClient(app)
    assert client.get("/ping").json() == {"ok": True}
    assert client.get("/api/ping").json() == {"ok": True}
