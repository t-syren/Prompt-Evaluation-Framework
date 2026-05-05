from fastapi import APIRouter, HTTPException
from backend.models.schemas import EvaluatRequest, EvaluateResponse
from backend.services.evaluator import evaluate_prompt, evaluate_dimensions, evaluate_safety

router = APIRouter()


@router.post("/evaluate", response_model=EvaluateResponse)
def evaluate(request: EvaluatRequest):
    try:
        return evaluate_prompt(request.prompt)
    except Exception as e:
        raise HTTPException(status_code=503, detail=str(e))


@router.post("/evaluate/dimensions", response_model=EvaluateResponse)
def evaluate_dims(request: EvaluatRequest):
    try:
        return EvaluateResponse(dimensions=evaluate_dimensions(request.prompt))
    except Exception as e:
        raise HTTPException(status_code=503, detail=str(e))


@router.post("/evaluate/safety", response_model=EvaluateResponse)
def evaluate_safe(request: EvaluatRequest):
    try:
        return EvaluateResponse(dimensions=evaluate_safety(request.prompt))
    except Exception as e:
        raise HTTPException(status_code=503, detail=str(e))
