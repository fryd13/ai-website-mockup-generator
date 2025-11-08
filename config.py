import os
from dotenv import load_dotenv
from pydantic import BaseModel

load_dotenv()
#Loading and assigning data from .env
class Settings(BaseModel):
	#OpenAI
	OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY")
	OPENAI_MODEL: str = "gpt-image-1-mini"
	IMAGE_SIZE: str = "1024x1536"

	#SMTP
	SMTP_SERVER: str = os.getenv("SMTP_SERVER")
	SMTP_PORT: int = int(os.getenv("SMTP_PORT"))
	SMTP_USERNAME: str = os.getenv("SMTP_USERNAME")
	SMTP_PASSWORD: str = os.getenv("SMTP_PASSWORD")
	SENDER_EMAIL: str = os.getenv("SENDER_EMAIL")

	#API
	API_URL: str = os.getenv("API_URL")
	IMAGE_STORAGE_PATH: str = os.getenv("IMAGE_STORAGE_PATH")
	MAX_RETRIES: int = int(os.getenv("MAX_RETRIES"))
	REQUEST_TIMEOUT: int = int(os.getenv("REQUEST_TIMEOUT"))

	#SECURITY
	SECRET_KEY: str = os.getenv("SECRET_KEY")
	ALLOWED_ORIGINS: list = os.getenv("ALLOWED_ORIGINS").split(",")
	ALLOWED_IPS: list = os.getenv("ALLOWED_IPS").split(",")

	LOG_DIR: str = os.getenv("LOG_DIR")

	class Config:
		env_file = ".env"
		case_sensitive = True
settings = Settings()

