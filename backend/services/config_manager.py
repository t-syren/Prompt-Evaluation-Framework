import json
import os
from pathlib import Path

CONFIG_PATH = Path(__file__).parent.parent.parent / "config.json"

DEFAULTS = {
    "auto_evaluate_after_fix": True,
    "auto_stress_test": False,
    "auto_hallucination_check": False,
    "auto_fix_prompt": False,
    "auto_evaluate_improvement": False,
    "stress_test_attack_count": 5,
    "iterative_fix_passes": 2,
}


class ConfigManager:
    def __init__(self, config_path: str = str(CONFIG_PATH)):
        self.config_path = Path(config_path)

    def load(self) -> dict:
        if self.config_path.exists():
            try:
                with open(self.config_path) as f:
                    data = json.load(f)
                for key, val in DEFAULTS.items():
                    data.setdefault(key, val)
                return data
            except json.JSONDecodeError as e:
                raise ValueError(f"Malformed config.json: {e}") from e

        base_url = os.getenv("DATABRICKS_BASE_URL")
        llm_url = os.getenv("LLM_ENDPOINT_URL")
        token = os.getenv("DATABRICKS_TOKEN")

        if not all([base_url, llm_url, token]):
            raise ValueError(
                "No configuration found. Please configure credentials in the Settings page."
            )

        return {
            "databricks_base_url": base_url,
            "llm_endpoint_url": llm_url,
            "api_token": token,
            **DEFAULTS,
        }

    def save(self, config: dict) -> None:
        self.config_path.parent.mkdir(parents=True, exist_ok=True)
        with open(self.config_path, "w") as f:
            json.dump(config, f, indent=2)


config_manager = ConfigManager()
