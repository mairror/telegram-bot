from telegram import Update
from utils.logging import logger

import telegram
from telegram.ext import (
    CallbackContext
)
import requests
import io
from typing import Dict
from config.settings import API_URL, API_KEY

# Enable logging
telegram_bot = logger("telegram_bot")


def send_photo_to_api(files: Dict):
    """
    Name: send_photo_to_api
    Description:
        Get a dictionary with a filename and a binary object and send to the API.
    Inputs:
        :files: type(dict): {"file": ("file_name", binary_object)}
    Outputs:
        None
    """
    data = {"source": "telegram"}
    headers = {"access_token": API_TOKEN}
    telegram_bot.debug(f"Sending the file object to the API.")
    try:
        r = requests.post(API_URL, files=files, data=data, headers=headers)
        if r.status_code == 201:
            telegram_bot.info(f"File sucessfully uploaded: {r.text}")
    except Exception as e:
        telegram_bot.error(f"There is an error when send the file: {e}.")



def start(update: Update, context: CallbackContext) -> None:
    """
    Name: start
    Description:
        Start callable function when /start command is used on the telegram bot. 
        Send a reply when using that command.
    Inputs: 
        :update: type(Update): update handler object.
        :context: type(CallbackContext).
    Outputs:
        None 
    """
    context.bot.send_message(chat_id=update.effective_chat.id, text="Welcome to mairror! Do you need to guess your age?")

def text(update: Update, context: CallbackContext) -> None:
    """
    Name: text
    Description:
        When a text message is sent in the telegram bot, the context send that message. 
    Inputs: 
        :update: type(Update): update handler object.
        :context: type(CallbackContext).
    Outputs:
        None 
    """
    context.bot.send_message(chat_id=update.effective_chat.id, text="Sorry, I didn't understand you.")

def unknown(update: Update, context: CallbackContext) -> None:
    """
    Name: unknown
    Description:
        When an unknown command is used the bot is replied with this message. 
    Inputs: 
        :update: type(Update): update handler object.
        :context: type(CallbackContext).
    Outputs:
        None 
    """
    context.bot.send_message(chat_id=update.effective_chat.id, text="Sorry, I didn't understand that command.")


def help_command(update: Update, context: CallbackContext) -> None:
    """
    Name: unknown
    Description:
        When used the /help command, you can get the command helper for the telegram bot. 
    Inputs: 
        :update: type(Update): update handler object.
        :context: type(CallbackContext).
    Outputs:
        None 
    """
    update.message.reply_text('Help!')


def photo(update: Update, context: CallbackContext) -> None:
    """
    Name: photo
    Description:
        Used to send a photo into the API when you uploaded in the telegram bot. 
    Inputs: 
        :update: type(Update): update handler object.
        :context: type(CallbackContext).
    Outputs:
        None 
    """
    files = {"file": (f"{update.message.photo[-1].file_unique_id}_{update.message.chat.id}.jpg",
                        io.BytesIO(update.message.photo[-1].get_file()))}
    send_photo_to_api(files)
