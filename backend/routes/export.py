from datetime import datetime, timezone
from fastapi import APIRouter
from fastapi.responses import JSONResponse
from backend.models.schemas import ExportRequest

router = APIRouter()


@router.post("/export")
def export(request: ExportRequest):
    payload = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "original_prompt": request.original_prompt,
        "evaluation": request.evaluation.model_dump(),
        "fixed_prompt": request.fixed_prompt,
        "variants": request.variants,
        "mode": request.mode,
        "stress_test_result": request.stress_test_result,
        "hallucination_result": request.hallucination_result,
    }
    return JSONResponse(
        content=payload,
        headers={"Content-Disposition": 'attachment; filename="pef_export.json"'},
    )
