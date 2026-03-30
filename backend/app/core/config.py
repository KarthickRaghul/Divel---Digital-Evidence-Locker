from pydantic_settings import BaseSettings
from pydantic import Field
from typing import Optional


class Settings(BaseSettings):
    # API
    API_V1_STR: str = "/api"
    PROJECT_NAME: str = "Digital Evidence Locker Backend"
    
    # AWS
    AWS_ACCESS_KEY_ID: Optional[str] = None
    AWS_SECRET_ACCESS_KEY: Optional[str] = None
    AWS_REGION: str = "eu-north-1"
    S3_BUCKET_NAME: Optional[str] = None
    DYNAMODB_TABLE_CASES: Optional[str] = None
    DYNAMODB_TABLE_EVIDENCE: Optional[str] = None

    # Blockchain
    BLOCKCHAIN_RPC_URL: str = "http://127.0.0.1:8545"
    BLOCKCHAIN_CONTRACT_ADDRESS: Optional[str] = None
    BLOCKCHAIN_PRIVATE_KEY: Optional[str] = None

    # AI
    GEMINI_API_KEY: Optional[str] = None
    AI_PROVIDER: str = "gemini" # Options: gemini, local
    OLLAMA_BASE_URL: str = "http://localhost:11434/api/generate"
    OLLAMA_MODEL: str = "llama3"

    # Security
    SECRET_KEY: str = Field(..., min_length=32)
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    class Config:
        env_file = ".env"
        case_sensitive = True
# Singleton instance
settings = Settings()
