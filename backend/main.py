from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.api.v1.endpoints import cases, evidence, auth

app = FastAPI(title=settings.PROJECT_NAME, openapi_url=f"{settings.API_V1_STR}/openapi.json")

# CORS
origins = [
    "http://localhost:5173", # Vite
    "http://localhost:3000",
    "*"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Routes
app.include_router(auth.router, prefix=f"{settings.API_V1_STR}/auth", tags=["auth"])
app.include_router(evidence.router, prefix=f"{settings.API_V1_STR}/evidence", tags=["evidence"])
app.include_router(cases.router, prefix=f"{settings.API_V1_STR}/cases", tags=["cases"])

@app.get("/")
def read_root():
    return {"message": "Welcome to Digital Evidence Locker API"}
