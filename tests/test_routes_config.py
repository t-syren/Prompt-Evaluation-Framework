from fastapi.testclient import TestClient
from unittest.mock import patch


def test_get_config_returns_masked_token():
    mock_cfg = {
        "databricks_base_url": "https://db.example.com",
        "llm_endpoint_url": "https://db.example.com/invocations",
        "api_token": "dapi_secret",
    }
    with patch("backend.routes.config.config_manager") as mock_mgr:
        mock_mgr.load.return_value = mock_cfg
        from backend.main import app
        client = TestClient(app)
        response = client.get("/config")
    assert response.status_code == 200
    data = response.json()
    assert data["api_token_set"] is True
    assert "dapi_secret" not in str(data)
    assert data["databricks_base_url"] == "https://db.example.com"


def test_post_config_saves_and_returns_success():
    payload = {
        "databricks_base_url": "https://new.example.com",
        "llm_endpoint_url": "https://new.example.com/invocations",
        "api_token": "dapi_new",
    }
    with patch("backend.routes.config.config_manager") as mock_mgr:
        mock_mgr.save.return_value = None
        from backend.main import app
        client = TestClient(app)
        response = client.post("/config", json=payload)
    assert response.status_code == 200
    assert response.json()["status"] == "saved"
    mock_mgr.save.assert_called_once()
