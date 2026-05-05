from fastapi import APIRouter
from backend.models.schemas import ConfigModel, ConfigResponse
from backend.services.config_manager import config_manager, DEFAULTS

router = APIRouter()


@router.get("/config", response_model=ConfigResponse)
def get_config():
    try:
        cfg = config_manager.load()
    except ValueError:
        return ConfigResponse(
            databricks_base_url="",
            llm_endpoint_url="",
            api_token_set=False,
        )
    return ConfigResponse(
        databricks_base_url=cfg["databricks_base_url"],
        llm_endpoint_url=cfg["llm_endpoint_url"],
        api_token_set=bool(cfg.get("api_token")),
        auto_evaluate_after_fix=cfg.get("auto_evaluate_after_fix", True),
        auto_stress_test=cfg.get("auto_stress_test", False),
        auto_hallucination_check=cfg.get("auto_hallucination_check", False),
        auto_fix_prompt=cfg.get("auto_fix_prompt", False),
        auto_evaluate_improvement=cfg.get("auto_evaluate_improvement", False),
        stress_test_attack_count=cfg.get("stress_test_attack_count", 5),
        iterative_fix_passes=cfg.get("iterative_fix_passes", 2),
    )


@router.post("/config")
def save_config(payload: ConfigModel):
    token = payload.api_token
    if not token:
        try:
            existing = config_manager.load()
            token = existing.get("api_token", "")
        except ValueError:
            token = ""
    config_manager.save({
        "databricks_base_url": payload.databricks_base_url,
        "llm_endpoint_url": payload.llm_endpoint_url,
        "api_token": token,
        "auto_evaluate_after_fix": payload.auto_evaluate_after_fix,
        "auto_stress_test": payload.auto_stress_test,
        "auto_hallucination_check": payload.auto_hallucination_check,
        "auto_fix_prompt": payload.auto_fix_prompt,
        "auto_evaluate_improvement": payload.auto_evaluate_improvement,
        "stress_test_attack_count": payload.stress_test_attack_count,
        "iterative_fix_passes": payload.iterative_fix_passes,
    })
    return {"status": "saved"}
