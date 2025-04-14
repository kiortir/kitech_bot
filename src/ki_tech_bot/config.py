from pathlib import Path
from pydantic import SecretStr
from pydantic_settings import BaseSettings


class Config(BaseSettings):
    bot_api_key: SecretStr
    the_cat_api_key: SecretStr
    storage_file_path: Path = Path("/storage.json")
