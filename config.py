from os.path import join, dirname
from pathlib import Path
from pydantic import SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict 

ROOT_DIR = Path(__file__).parent.parent

class Config(BaseSettings):
    Bot_Tocken: SecretStr #str 
    API_KEY: SecretStr
    Admin: int

    model_config = SettingsConfigDict(
        env_file=ROOT_DIR / "src" / ".env",
        env_file_encoding="utf-8",
        extra="ignore"
    )

config = Config()