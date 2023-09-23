import os
from bot.bot_logic import start, help_command, enano, matias, chatbot
from telegram.ext import CommandHandler, Application

TELEGRAM_API_TOKEN = os.environ.get("TELEGRAM_API_TOKEN")


def main():
    app = Application.builder().token(TELEGRAM_API_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("enano", enano))
    app.add_handler(CommandHandler("matias", matias))
    app.add_handler(CommandHandler("ai", chatbot))

    app.run_polling()


if __name__ == "__main__":
    main()
