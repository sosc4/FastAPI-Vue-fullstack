from dotenv import load_dotenv
from pydantic_settings import BaseSettings

load_dotenv()


class Settings(BaseSettings):
    JWT_SECRET_KEY: str = "change_me"
    ADMIN_USERNAME: str = "admin"
    ADMIN_INIT_PASSWORD: str = "admin"


settings = Settings()
