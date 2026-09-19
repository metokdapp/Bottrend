import threading
import time

import requests
import config
from collector import build_all_in_one_payload
from ai_analyzer import analyze_payload_with_gemini
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

rc = set()


def run(cid, token):
    cc = 1
    while cid in rc:
        p = build_all_in_one_payload(cc)
        d = analyze_payload_with_gemini(p)
        action = d.get("action")
        msg = f"🚨 *BOTTREND* 🚨\nAction: {action}"
        requests.post(
            f"https://api.telegram.org/bot{token}/sendMessage",
            json={"chat_id": cid, "text": msg, "parse_mode": "Markdown"},
            timeout=15,
        )
        cc += 1
        for _ in range(60):
            if cid not in rc:
                break
            time.sleep(1)


async def start(u: Update, c: ContextTypes.DEFAULT_TYPE):
    chat_id = u.effective_chat.id
    if chat_id not in rc:
        rc.add(chat_id)
        await u.message.reply_text("🚀 Bottrend ĐÃ BẬT!")
        threading.Thread(target=run, args=(chat_id, config.TELEGRAM_BOT_TOKEN), daemon=True).start()


async def stop(u: Update, c: ContextTypes.DEFAULT_TYPE):
    chat_id = u.effective_chat.id
    if chat_id in rc:
        rc.remove(chat_id)
        await u.message.reply_text("🛑 Bottrend ĐÃ DỪNG!")


def main():
    app = ApplicationBuilder().token(config.TELEGRAM_BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("stop", stop))
    app.run_polling()


if __name__ == "__main__":
    main()
