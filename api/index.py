import os
from bot.bot_logic import (
    start,
    help_command,
    chatbot,
    file_handler,
    add_admin_to_whitelist,
    query_bot,
)
from telegram.ext import CommandHandler, Application, MessageHandler, filters

TELEGRAM_API_TOKEN = os.environ.get("TELEGRAM_API_TOKEN")


def main():
    try:
        app = Application.builder().token(TELEGRAM_API_TOKEN).build()

        app.add_handler(CommandHandler("start", start))
        app.add_handler(CommandHandler("help", help_command))
        app.add_handler(CommandHandler("ai", chatbot))
        app.add_handler(MessageHandler(filters.ATTACHMENT, file_handler))
        app.add_handler(CommandHandler("add_admin", add_admin_to_whitelist))
        app.add_handler(CommandHandler("query", query_bot))

        app.run_polling()
    except Exception as e:
        # Handle exceptions gracefully, e.g., log the error and send an alert
        print(f"An error occurred: {e}")
        # You can implement your custom error handling logic here


if __name__ == "__main__":
    main()