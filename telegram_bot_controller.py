import asyncio
import logging
import threading
import time

import config
from ai_analyzer import analyze_payload_with_gemini
from collector import build_all_in_one_payload
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

logger = logging.getLogger(__name__)
running_chats = set()


def report_loop(chat_id, bot, interval_seconds):
    cycle_id = 1
    while chat_id in running_chats:
        try:
            payload = build_all_in_one_payload(cycle_id)
            decision = analyze_payload_with_gemini(payload)
            message = (
                "₿ BTC/USDT — AI REPORT\n"
                f"Action: {decision.get('action', 'HOLD')}\n"
                f"Confidence: {decision.get('confidence', 0)}%\n"
                f"Reason: {decision.get('reason', 'Không có lý do.')}"
            )
            asyncio.run(bot.send_message(chat_id=chat_id, text=message))
        except Exception:
            logger.exception("Report cycle failed for chat %s", chat_id)
        cycle_id += 1
        for _ in range(interval_seconds):
            if chat_id not in running_chats:
                return
            time.sleep(1)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    if chat_id in running_chats:
        await update.message.reply_text("Bottrend đang chạy.")
        return
    running_chats.add(chat_id)
    await update.message.reply_text(f"🚀 Bottrend đã bật. Báo cáo mỗi {config.INTERVAL_MINUTES} phút.")
    threading.Thread(
        target=report_loop,
        args=(chat_id, context.bot, config.INTERVAL_MINUTES * 60),
        daemon=True,
    ).start()


async def stop(update: Update, context: ContextTypes.DEFAULT_TYPE):
    running_chats.discard(update.effective_chat.id)
    await update.message.reply_text("🛑 Bottrend đã dừng.")


async def status(update: Update, context: ContextTypes.DEFAULT_TYPE):
    state = "ĐANG CHẠY" if update.effective_chat.id in running_chats else "ĐANG DỪNG"
    await update.message.reply_text(f"Bottrend: {state}")


def main():
    if not config.TELEGRAM_BOT_TOKEN:
        raise RuntimeError("Missing TELEGRAM_BOT_TOKEN")
    app = ApplicationBuilder().token(config.TELEGRAM_BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("stop", stop))
    app.add_handler(CommandHandler("status", status))
    app.run_polling(drop_pending_updates=True)


if __name__ == "__main__":
    main()
