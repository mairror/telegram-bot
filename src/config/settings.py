import os

from dotenv import load_dotenv

if os.path.exists(".env"):
    load_dotenv()

BOT_TELEGRAM_TOKEN = os.getenv("BOT_TELEGRAM_TOKEN", "test_token")
API_KEY = os.getenv("API_KEY", "test")
API_URL = os.getenv("API_URL", "http://localhost:8000")
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
API_UPLOAD_PATH = os.getenv("API_UPLOAD_PATH", "/images/upload")
API_PREDICT_PATH = os.getenv("API_PREDICT_PATH", "/images/predict")
SLACK_WEBHOOK_URI = os.getenv("SLACK_WEBHOOK_URI", "xxxxx")
