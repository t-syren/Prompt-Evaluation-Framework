from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.routes import config, evaluate, fix, export, advanced

app = FastAPI(title="PEF API", version="2.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(config.router)
app.include_router(evaluate.router)
app.include_router(fix.router)
app.include_router(export.router)
app.include_router(advanced.router)
