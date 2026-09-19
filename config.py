import os

GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")
GEMINI_MODEL = os.environ.get("GEMINI_MODEL", "gemini-2.5-flash")
TELEGRAM_BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")
CMC_API_KEY = os.environ.get("CMC_API_KEY")
INTERVAL_MINUTES = max(1, int(os.environ.get("INTERVAL_MINUTES", "15")))
