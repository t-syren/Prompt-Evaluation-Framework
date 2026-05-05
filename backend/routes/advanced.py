from fastapi import APIRouter, HTTPException
from backend.models.schemas import (
    StressTestRequest, StressTestResponse,
    HallucinationCheckRequest, HallucinationCheckResponse,
)
from backend.services.stress_tester import run_stress_test
from backend.services.hallucination import check_hallucination

router = APIRouter()


@router.post("/stress-test", response_model=StressTestResponse)
def stress_test(request: StressTestRequest):
    try:
        return run_stress_test(request.prompt, num_attacks=request.num_attacks)
    except Exception as e:
        raise HTTPException(status_code=503, detail=str(e))


@router.post("/hallucination-check", response_model=HallucinationCheckResponse)
def hallucination_check(request: HallucinationCheckRequest):
    try:
        return check_hallucination(request.prompt)
    except Exception as e:
        raise HTTPException(status_code=503, detail=str(e))
