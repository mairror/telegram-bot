from typing import Dict

import requests
from config.settings import API_KEY, API_PREDICT_PATH, API_UPLOAD_PATH, API_URL
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import CallbackContext
from utils.logging import telegram_bot


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
    telegram_bot.debug("Sending the file object to the API.")
    try:
        r = requests.post(
            API_URL + API_UPLOAD_PATH, files=files, data=data, headers=headers
        )
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
    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="Welcome to mairror! Do you need to guess your age?",
    )


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
    context.bot.send_message(
        chat_id=update.effective_chat.id, text="Sorry, I didn't understand you."
    )


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
    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="Sorry, I didn't understand that command.",
    )


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
    update.message.reply_text(
        """
<b>Mairror Bot:</b>

You can find <a href="https://github.com/mairror/telegram-bot/blob/main/README.md">here</a> this bot's documentation.
Authors of this bot:

    - <a href="https://www.linkedin.com/in/%E2%9C%85-borja-l-422666a9">Borja</a>
    - <a href="https://www.linkedin.com/in/aacecan">Alex</a>
        """,
        parse_mode="HTML",
        disable_web_page_preview=True,
    )


async def predict(image):
    data = {"key": image}
    headers = {"X-Api-Key": API_KEY}
    telegram_bot.debug(f"Predict image {image}.")
    try:
        r = await requests.post(API_URL + API_PREDICT_PATH, data=data, headers=headers)
        if r.status_code == 200:
            telegram_bot.info(f"Sucessfully predicted: {r.text}")
            return r.text
    except Exception as e:
        telegram_bot.error(f"There is an error when send the file: {e}.")


def keyboard():
    keyboard = [
        [
            InlineKeyboardButton("Yes!!!", callback_data="yes"),
            InlineKeyboardButton("No", callback_data="no"),
        ],
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)
    return reply_markup


def button(update: Update, context: CallbackContext) -> None:
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
    query = update.callback_query
    query.answer()
    if query.data == "yes":
        query.edit_message_text(text="I'm a great guesser!")
    else:
        query.edit_message_text(
            text="Sorry, I'll do the best of me. I need more images to improve the prediction."
        )


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
    image = f"{update.message.photo[-1].file_unique_id}_{update.message.chat.id}.jpg"
    files = {
        "file": (
            # AQADFrkxG-3bCVFy_3235057.jpg
            image,
            bytes(update.message.photo[-1].get_file().download_as_bytearray()),
        )
    }
    send_photo_to_api(files)
    context.bot.send_chat_action(chat_id=update.effective_chat.id, action="typing")
    prediction = predict(image)
    if prediction:
        context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=f"""
<b>PREDICTION:</b>

<b>AGE: </b>{prediction["age"]}
<b>GENDER: </b>{prediction["gender"]}
        """,
            parse_mode="HTML",
            disable_web_page_preview=True,
        )
    reply_markup = keyboard()
    update.message.reply_text("Have I guessed your age?", reply_markup=reply_markup)
