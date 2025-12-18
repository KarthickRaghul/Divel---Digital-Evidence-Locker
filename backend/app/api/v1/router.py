from fastapi import APIRouter
from app.api.v1.routes import auth, evidence, case, audit

api_router = APIRouter()

api_router.include_router(auth.router, prefix="/auth", tags=["Auth"])
api_router.include_router(evidence.router, prefix="/evidence", tags=["Evidence"])
api_router.include_router(case.router, prefix="/case", tags=["Case"])
api_router.include_router(audit.router, prefix="/audit", tags=["Audit"])
