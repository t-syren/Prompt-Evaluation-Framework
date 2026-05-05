from fastapi import APIRouter, HTTPException
from backend.models.schemas import (
    FixRequest, FixResponse, RefineRequest,
    FixValidateRequest, FixValidateResponse,
)
from backend.services.fixer import fix_prompt, refine_prompt, validate_fix

router = APIRouter()


@router.post("/fix", response_model=FixResponse)
def fix(request: FixRequest):
    try:
        return fix_prompt(request.prompt, request.evaluation, request.mode)
    except Exception as e:
        raise HTTPException(status_code=503, detail=str(e))


@router.post("/fix/generate", response_model=FixResponse)
def fix_generate(request: FixRequest):
    try:
        return fix_prompt(request.prompt, request.evaluation, request.mode)
    except Exception as e:
        raise HTTPException(status_code=503, detail=str(e))


@router.post("/fix/validate", response_model=FixValidateResponse)
def fix_validate(request: FixValidateRequest):
    try:
        return validate_fix(request.original_prompt, request.fixed_prompt, request.original_evaluation)
    except Exception as e:
        raise HTTPException(status_code=503, detail=str(e))


@router.post("/refine", response_model=FixResponse)
def refine(request: RefineRequest):
    try:
        return refine_prompt(
            request.original_prompt,
            request.current_fixed,
            request.evaluation,
            request.feedback,
            request.mode,
        )
    except Exception as e:
        raise HTTPException(status_code=503, detail=str(e))
