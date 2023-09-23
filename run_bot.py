from bot import bot_logic  # Import your bot's logic from bot_logic.py
from telegram.ext import Updater


def main():
    # Initialize the bot
    updater = Updater(token=bot_logic.TOKEN, use_context=True)
    dispatcher = updater.dispatcher

    # Register your bot's handlers
    bot_logic.register_handlers(dispatcher)

    # Start the bot
    updater.start_polling()
    updater.idle()


if __name__ == "__main__":
    main()
