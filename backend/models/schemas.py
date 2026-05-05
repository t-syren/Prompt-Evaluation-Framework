from typing import Literal, Optional
from pydantic import BaseModel, Field


class Dimension(BaseModel):
    name: str
    score: int = Field(..., ge=1, le=10)
    issues: list[str]
    suggestions: list[str]
    reasoning: Optional[str] = None


class EvaluateResponse(BaseModel):
    dimensions: list[Dimension]


class EvaluatRequest(BaseModel):
    prompt: str = Field(..., min_length=1)


class FixRequest(BaseModel):
    prompt: str = Field(..., min_length=1)
    evaluation: EvaluateResponse
    mode: Literal["single", "variants"]


class RefineRequest(BaseModel):
    original_prompt: str = Field(..., min_length=1)
    current_fixed: str = Field(..., min_length=1)
    evaluation: EvaluateResponse
    feedback: str = Field(..., min_length=1)
    mode: Literal["single", "variants"] = "single"


class FixResponse(BaseModel):
    fixed_prompt: Optional[str] = None
    variants: Optional[list[str]] = None


class RegressionWarning(BaseModel):
    dimension: str
    original_score: int
    fixed_score: int


class FixValidateRequest(BaseModel):
    original_prompt: str = Field(..., min_length=1)
    fixed_prompt: str = Field(..., min_length=1)
    original_evaluation: EvaluateResponse


class FixValidateResponse(BaseModel):
    post_eval: EvaluateResponse
    regression_warnings: list[RegressionWarning]
    safety_warnings: list[str]


class AttackResult(BaseModel):
    input: str
    attack_type: str
    verdict: str
    reason: str


class StressTestRequest(BaseModel):
    prompt: str = Field(..., min_length=1)
    num_attacks: int = Field(default=5, ge=1, le=10)


class StressTestResponse(BaseModel):
    attacks: list[AttackResult]
    vulnerability_score: int = Field(..., ge=1, le=10)


class HallucinationCheckRequest(BaseModel):
    prompt: str = Field(..., min_length=1)


class HallucinationCheckResponse(BaseModel):
    sample_output: str
    hallucination_score: int = Field(..., ge=1, le=10)
    verdict: str
    reason: str


class DefaultsConfig(BaseModel):
    auto_evaluate_after_fix: bool = True
    auto_stress_test: bool = False
    auto_hallucination_check: bool = False
    auto_fix_prompt: bool = False
    auto_evaluate_improvement: bool = False
    stress_test_attack_count: int = Field(default=5, ge=1, le=10)
    iterative_fix_passes: int = Field(default=2, ge=1, le=3)


class ExportRequest(BaseModel):
    original_prompt: str
    evaluation: EvaluateResponse
    fixed_prompt: Optional[str] = None
    variants: Optional[list[str]] = None
    mode: Literal["single", "variants"] = "single"
    stress_test_result: Optional[dict] = None
    hallucination_result: Optional[dict] = None


class ConfigModel(BaseModel):
    databricks_base_url: str
    llm_endpoint_url: str
    api_token: Optional[str] = None
    auto_evaluate_after_fix: bool = True
    auto_stress_test: bool = False
    auto_hallucination_check: bool = False
    auto_fix_prompt: bool = False
    auto_evaluate_improvement: bool = False
    stress_test_attack_count: int = 5
    iterative_fix_passes: int = 2


class ConfigResponse(BaseModel):
    databricks_base_url: str
    llm_endpoint_url: str
    api_token_set: bool
    auto_evaluate_after_fix: bool = True
    auto_stress_test: bool = False
    auto_hallucination_check: bool = False
    auto_fix_prompt: bool = False
    auto_evaluate_improvement: bool = False
    stress_test_attack_count: int = 5
    iterative_fix_passes: int = 2
