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

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
# set higher logging level for httpx to avoid all GET and POST requests being logged
logging.getLogger("httpx").setLevel(logging.WARNING)

logger = logging.getLogger(__name__)


# Define a few command handlers. These usually take the two arguments update and
# context.
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /start is issued."""
    user = update.effective_user


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /help is issued."""
    await update.message.reply_text(
        "Para utilizar el bot, escriba /ai y luego tu mensaje"
    )


async def chatbot(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    message_text = update.message.text[len("/ai ") :]
    await context.bot.send_chat_action(
        chat_id=update.effective_chat.id, action="typing"
    )
    response = ai_bot.chat(message_text)
    await update.message.reply_text(response)


# function that handles a file sent by an user
async def file_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    try:
        if update.effective_user.id not in context.bot_data["whitelist"]:
            await update.message.reply_text("No eres un usuario autorizado")
            return
        if update.message.document.mime_type != "application/pdf":
            await update.message.reply_text("El archivo no es un pdf")
            return

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

        await update.message.reply_text("El bot ha sido entrenado")
    except Exception as e:
        print(e)
        await update.message.reply_text("Error al entrenar el bot")


# add the admin to the whitelist automatically
async def add_admin_to_whitelist(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> None:
    # create the whitelist if it doesn't exist
    if "whitelist" not in context.bot_data:
        context.bot_data["whitelist"] = []
    if update.effective_user.id not in context.bot_data["whitelist"]:
        context.bot_data["whitelist"].append(update.effective_user.id)
        await update.message.reply_text("Usuario añadido a la whitelist")
    else:
        await update.message.reply_text("El usuario ya está en la whitelist")


# function that query the bot
async def query_bot(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    try:
        message_text = update.message.text[len("/query ") :]
        await context.bot.send_chat_action(
            chat_id=update.effective_chat.id, action="typing"
        )
        response = query(message_text)
        await update.message.reply_text(response)
    except Exception as e:
        print(e)
        await update.message.reply_text("Error al consultar el bot")
