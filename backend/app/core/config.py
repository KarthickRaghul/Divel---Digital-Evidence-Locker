from pydantic import BaseSettings

class Settings(BaseSettings):
    APP_NAME: str = "DIVEL"
    AWS_REGION: str
    S3_BUCKET_NAME: str
    JWT_SECRET: str

    class Config:
        env_file = ".env"

settings = Settings()
