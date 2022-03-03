from telegram import Update
from utils.logging import telegram_bot

import telegram
from telegram.ext import (
    CallbackContext
)
import requests
from typing import Dict
from config.settings import API_URL, API_KEY, API_UPLOAD_PATH




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
    headers = {"X-Api-Key": API_KEY}
    telegram_bot.debug(f"Sending the file object to the API.")
    try:
        r = requests.post(API_URL + API_UPLOAD_PATH, files=files, data=data, headers=headers)
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
    update.message.reply_text('''
<b>Mairror Bot:</b>

You can find <a href="https://github.com/mairror/telegram-bot/blob/main/README.md">here</a> this bot's documentation.
Authors of this bot:

    - <a href="https://www.linkedin.com/in/%E2%9C%85-borja-l-422666a9">Borja</a>
    - <a href="https://www.linkedin.com/in/aacecan">Alex</a>
        ''', parse_mode="HTML", disable_web_page_preview=True)


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
    files = {
        "file": (
            # AQADFrkxG-3bCVFy_3235057.jpg
            f"{update.message.photo[-1].file_unique_id}_{update.message.chat.id}.jpg",
                        bytes(update.message.photo[-1].get_file().download_as_bytearray()))}
    send_photo_to_api(files)
