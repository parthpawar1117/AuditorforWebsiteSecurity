import importlib

import pytest
from fastapi.testclient import TestClient

from backend.app.api.routes import resolve_demo_target


# --- resolve_demo_target: hosted demo may only scan its own test bench -------

@pytest.mark.parametrize("path", ["/mock/hardened", "/mock/balanced", "/mock/vulnerable"])
def test_demo_target_rewrites_test_bench_to_own_host(path):
    # The UI's preset buttons still say 127.0.0.1:8000 — the hosted app scans itself instead.
    target = resolve_demo_target(f"https://127.0.0.1:8000{path}", "https://cybersentinel.example.app/")
    assert target == f"https://cybersentinel.example.app{path}"


def test_demo_target_forces_https_for_public_hosts():
    target = resolve_demo_target("https://x/mock/hardened", "http://cybersentinel.example.app/")
    assert target.startswith("https://cybersentinel.example.app")


def test_demo_target_keeps_http_on_localhost():
    target = resolve_demo_target("https://x/mock/balanced", "http://127.0.0.1:8000/")
    assert target == "http://127.0.0.1:8000/mock/balanced"


@pytest.mark.parametrize("url", ["https://example.com", "https://example.com/mock/hardened/../admin", "https://127.0.0.1:8000/api/scans"])
def test_demo_target_rejects_anything_else(url):
    with pytest.raises(ValueError):
        resolve_demo_target(url, "https://cybersentinel.example.app/")


# --- config: demo mode and DB path come from the environment -----------------

def test_config_reads_demo_mode_and_db_path(monkeypatch, tmp_path):
    monkeypatch.setenv("CYBERSENTINEL_DEMO_MODE", "1")
    monkeypatch.setenv("CYBERSENTINEL_DB_PATH", str(tmp_path / "demo.db"))
    import backend.app.core.config as config

    config = importlib.reload(config)
    assert config.DEMO_MODE is True
    assert str(config.DB_PATH) == str(tmp_path / "demo.db")

    monkeypatch.delenv("CYBERSENTINEL_DEMO_MODE")
    monkeypatch.delenv("CYBERSENTINEL_DB_PATH")
    config = importlib.reload(config)
    assert config.DEMO_MODE is False
    assert config.DB_PATH.name == "cybersentinel.db"


# --- API: in demo mode an external target is refused before any request ------

def test_scan_endpoint_refuses_external_targets_in_demo_mode(monkeypatch):
    import backend.app.api.routes as routes

    monkeypatch.setattr(routes, "DEMO_MODE", True)
    from backend.app.main import app

    res = TestClient(app).post("/api/scan", json={"target_url": "https://example.com"})
    assert res.status_code == 400
    assert "test bench" in res.json()["detail"]
