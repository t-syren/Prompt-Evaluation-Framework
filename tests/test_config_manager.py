import json
import os
import pytest
from unittest.mock import patch
from backend.services.config_manager import ConfigManager


def test_load_from_config_json(tmp_path):
    cfg_file = tmp_path / "config.json"
    cfg_file.write_text(json.dumps({
        "databricks_base_url": "https://db.example.com",
        "llm_endpoint_url": "https://db.example.com/invocations",
        "api_token": "dapi_test"
    }))
    manager = ConfigManager(config_path=str(cfg_file))
    cfg = manager.load()
    assert cfg["api_token"] == "dapi_test"
    assert cfg["databricks_base_url"] == "https://db.example.com"


def test_load_falls_back_to_env(tmp_path):
    cfg_file = tmp_path / "config.json"  # does not exist
    env_vars = {
        "DATABRICKS_BASE_URL": "https://env.example.com",
        "LLM_ENDPOINT_URL": "https://env.example.com/invocations",
        "DATABRICKS_TOKEN": "dapi_env",
    }
    with patch.dict(os.environ, env_vars):
        manager = ConfigManager(config_path=str(cfg_file))
        cfg = manager.load()
    assert cfg["api_token"] == "dapi_env"
    assert cfg["databricks_base_url"] == "https://env.example.com"


def test_save_writes_config_json(tmp_path):
    cfg_file = tmp_path / "config.json"
    manager = ConfigManager(config_path=str(cfg_file))
    manager.save({
        "databricks_base_url": "https://new.example.com",
        "llm_endpoint_url": "https://new.example.com/invocations",
        "api_token": "dapi_new"
    })
    saved = json.loads(cfg_file.read_text())
    assert saved["api_token"] == "dapi_new"


def test_load_raises_when_no_config_and_no_env(tmp_path):
    cfg_file = tmp_path / "config.json"
    with patch.dict(os.environ, {}, clear=True):
        manager = ConfigManager(config_path=str(cfg_file))
        with pytest.raises(ValueError, match="No configuration found"):
            manager.load()


def test_load_returns_defaults_when_fields_missing(tmp_path):
    cfg_file = tmp_path / "config.json"
    cfg_file.write_text('{"databricks_base_url":"https://db.example.com","llm_endpoint_url":"https://db.example.com/invocations","api_token":"tok"}')
    manager = ConfigManager(config_path=str(cfg_file))
    cfg = manager.load()
    assert cfg["auto_evaluate_after_fix"] is True
    assert cfg["auto_stress_test"] is False
    assert cfg["stress_test_attack_count"] == 5
    assert cfg["iterative_fix_passes"] == 2


def test_save_and_load_defaults(tmp_path):
    cfg_file = tmp_path / "config.json"
    manager = ConfigManager(config_path=str(cfg_file))
    manager.save({
        "databricks_base_url": "https://db.example.com",
        "llm_endpoint_url": "https://db.example.com/invocations",
        "api_token": "tok",
        "auto_evaluate_after_fix": False,
        "auto_stress_test": True,
        "auto_hallucination_check": True,
        "stress_test_attack_count": 10,
        "iterative_fix_passes": 3,
    })
    cfg = manager.load()
    assert cfg["auto_evaluate_after_fix"] is False
    assert cfg["auto_stress_test"] is True
    assert cfg["stress_test_attack_count"] == 10
