from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    # API
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "Digital Evidence Locker Backend"
    
    # AWS
    AWS_ACCESS_KEY_ID: Optional[str] = None
    AWS_SECRET_ACCESS_KEY: Optional[str] = None
    AWS_REGION: str = "eu-north-1"
    S3_BUCKET_NAME: Optional[str] = None
    DYNAMODB_TABLE_CASES: str = "cases"
    DYNAMODB_TABLE_EVIDENCE: str = "evidence"

    # Blockchain
    BLOCKCHAIN_RPC_URL: str = "http://127.0.0.1:8545"
    BLOCKCHAIN_CONTRACT_ADDRESS: Optional[str] = None
    BLOCKCHAIN_PRIVATE_KEY: Optional[str] = None

    # AI
    OPENAI_API_KEY: Optional[str] = None

    # Security
    SECRET_KEY: str = "supersecretkeydefaultsfortestingonly"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    class Config:
        env_file = ".env"

settings = Settings()
