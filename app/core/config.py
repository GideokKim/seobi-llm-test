from pydantic_settings import BaseSettings, SettingsConfigDict
from functools import lru_cache
from typing import Optional, List
import os
import logging
from pathlib import Path

# 로깅 설정
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# 프로젝트 루트 디렉토리 찾기
ROOT_DIR = Path(__file__).resolve().parent.parent.parent
ENV_FILE = ROOT_DIR / ".env"

logger.info(f"Looking for .env file at: {ENV_FILE}")

class Settings(BaseSettings):
    # Azure OpenAI 설정
    azure_openai_api_key: str = os.getenv("AZURE_OPENAI_API_KEY", "dummy-key")
    azure_openai_endpoint: str = os.getenv("AZURE_OPENAI_ENDPOINT", "https://dummy-endpoint.openai.azure.com/")
    azure_openai_api_version: str = os.getenv("AZURE_OPENAI_API_VERSION", "2024-02-15-preview")
    azure_openai_deployment_name: str = os.getenv("AZURE_OPENAI_DEPLOYMENT_NAME", "dummy-deployment")

    # 데이터베이스 설정
    database_url: str = f"sqlite:///{os.path.join(os.path.dirname(os.path.dirname(__file__)), 'app.db')}"

    # 애플리케이션 설정
    secret_key: str = os.getenv("SECRET_KEY", "dev-secret-key")
    environment: str = os.getenv("ENVIRONMENT", "development")
    
    # CORS 설정
    cors_origins: List[str] = ["http://localhost:3000"]  # 프론트엔드 URL

    model_config = SettingsConfigDict(
        env_file=str(ENV_FILE),
        env_file_encoding='utf-8',
        case_sensitive=True,
        extra="allow"  # 추가 필드 허용
    )

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        logger.info(f"Loaded settings from .env file: {ENV_FILE.exists()}")
        logger.info(f"Environment: {self.environment}")
        logger.info(f"Azure OpenAI endpoint: {self.azure_openai_endpoint}")
        logger.info(f"Azure OpenAI deployment: {self.azure_openai_deployment_name}")
        # API 키는 보안상 로깅하지 않습니다

        if self.environment == "development":
            logger.warning("Running in development mode with dummy values")
            if self.azure_openai_api_key == "dummy-key":
                logger.warning("Using dummy Azure OpenAI API key")
            if "dummy-endpoint" in self.azure_openai_endpoint:
                logger.warning("Using dummy Azure OpenAI endpoint")
            if self.azure_openai_deployment_name == "dummy-deployment":
                logger.warning("Using dummy Azure OpenAI deployment name")


@lru_cache()
def get_settings() -> Settings:
    settings = Settings()
    return settings 