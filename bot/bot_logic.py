import logging, os

from telegram import ForceReply, Update
from telegram.ext import (
    ContextTypes,
)
from .chatbot import ChatBot
from .pdf_to_md import convert_pdf_to_md
from .train import train_bot
from .query import query

ai_bot = ChatBot()
default_whitelist = ["elmatero"]

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
# Set a higher logging level for httpx to avoid all GET and POST requests being logged
logging.getLogger("httpx").setLevel(logging.WARNING)

logger = logging.getLogger(__name__)


# Define a few command handlers. These usually take the two arguments update and
# context.
async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /help is issued."""
    await update.message.reply_text("To use the bot, type /ai and then your message")


# Function that handles a file sent by a user
async def file_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    try:
        if update.message.chat.type == "private":
            if "whitelist" not in context.bot_data:
                context.bot_data["whitelist"] = default_whitelist
            logger.info(
                "update %s %s",
                update.effective_user.username,
                context.bot_data["whitelist"],
            )
            if update.effective_user.username not in context.bot_data["whitelist"]:
                return await update.message.reply_text("You are not an authorized user")
            if update.message.document.mime_type != "application/pdf":
                return await update.message.reply_text("The file is not a PDF")

            file = await update.message.document.get_file()

            for filename in os.listdir("data/pdfs"):
                os.remove(f"data/pdfs/{filename}")
            for filename in os.listdir("data/md"):
                os.remove(f"data/md/{filename}")

            await file.download_to_drive(custom_path=f"data/pdfs/file.pdf")
            convert_pdf_to_md()

            for filename in os.listdir("data/storage"):
                os.remove(f"data/storage/{filename}")

            train_bot()

            await update.message.reply_text("The bot has been trained")
    except Exception as e:
        logger.error(e)
        await update.message.reply_text("Error training the bot")


# Add the admin to the whitelist automatically
async def add_admin_to_whitelist(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> None:
    message_text = update.message.text[len("/add_admin ") :]
    logger.info(update.effective_user)
    logger.info(message_text)

    # Create the whitelist if it doesn't exist
    if "whitelist" not in context.bot_data:
        context.bot_data["whitelist"] = default_whitelist
    logger.info(context.bot_data["whitelist"])
    if message_text == "":
        return await update.message.reply_text(
            "Please enter a username after the command"
        )
    if message_text not in context.bot_data["whitelist"]:
        context.bot_data["whitelist"].append(message_text)
        return await update.message.reply_text("User added to the whitelist")
    else:
        return await update.message.reply_text("The user is already in the whitelist")


# Function that queries the bot
async def ai(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    try:
        message_text = update.message.text[len("/ai ") :]
        await context.bot.send_chat_action(
            chat_id=update.effective_chat.id, action="typing"
        )
        response = query(message_text)
        logger.info("%s %s", update.effective_user.username, message_text)
        logger.info("Chatbot %s", response)
        await update.message.reply_text(response)
    except Exception as e:
        logger.error(e)
        await update.message.reply_text("Error, please try again later")


async def chatbot(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    message_text = update.message.text[len("/ai ") :]
    await context.bot.send_chat_action(
        chat_id=update.effective_chat.id, action="typing"
    )
    response = ai_bot.chat(message_text)
    await update.message.reply_text(response)
