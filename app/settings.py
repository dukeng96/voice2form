from pydantic import BaseSettings, Field

class Settings(BaseSettings):
    llm_endpoint: str = Field(..., env="LLM_ENDPOINT")
    stt_endpoint: str = Field(..., env="STT_ENDPOINT")

    class Config:
        env_file = ".env"


def get_settings():
    return Settings()
