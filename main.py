import logging
from telegram_bot_controller import main as run_telegram_bot

logging.basicConfig(level=logging.INFO, format="%(asctime)s | %(levelname)s | %(name)s | %(message)s")

if __name__ == "__main__":
    run_telegram_bot()
