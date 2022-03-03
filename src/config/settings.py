from dotenv import load_dotenv
import os


if os.path.exists(".env"):
    load_dotenv()

BOT_TELEGRAM_TOKEN = os.getenv("BOT_TELEGRAM_TOKEN", "test_token")
API_KEY = os.getenv("API_KEY", "test_key")
API_URL = os.getenv("API_URL", "http://localhost:8001")
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
