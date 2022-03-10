import json
import time
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
        telegram_bot.error(f"There was an error sending the file: {e}.")


def keyboard():
    keyboard = [
        [
            InlineKeyboardButton("Yes!!!", callback_data="yes"),
            InlineKeyboardButton("No", callback_data="no"),
        ],
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)
    return reply_markup


def keyboard_start():
    keyboard = [
        [
            InlineKeyboardButton("Yes!!!", callback_data="YES"),
            InlineKeyboardButton("No", callback_data="NO"),
        ],
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)
    return reply_markup


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
    reply_markup = keyboard_start()
    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="Welcome to mairror! Do you want me to guess your age?",
        reply_markup=reply_markup,
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
        chat_id=update.effective_chat.id,
        text="Sorry, I didn't understand you. Please send me a pic.",
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


def build_text_prediction(prediction: Dict):
    newline = "\n"
    text = f"""
<b>PREDICTION:</b>\n
{newline.join([f"Face {count+1}: (Age: {pred['age']}), (Gender: {pred['gender']})"
                for count, pred in enumerate(prediction["predictions"]) ])}
"""
    return text


def predict(image):
    data = {"image_id": image}
    print(data)
    headers = {"X-Api-Key": API_KEY}
    telegram_bot.debug(f"Predict image {image}.")
    try:
        r = requests.post(
            API_URL + API_PREDICT_PATH, data=json.dumps(data), headers=headers
        )
        if r.status_code == 200:
            telegram_bot.info(f"Sucessfully predicted: {r.text}")
            return build_text_prediction(json.loads(r.text))
        else:
            telegram_bot.error(f"Error querying the API: {r.text}.")
            return "There was an error predicting your image."
    except Exception as e:
        telegram_bot.error(f"There is an error making the prediction: {e}.")


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
    answer = query.data
    if answer == "yes":
        query.edit_message_text(text="I'm a great guesser!")
    elif answer == "YES":
        query.edit_message_text(
            text="To start please send me a pic of yourself and I will try to guess your age and gender."
        )
    elif answer == "NO":
        query.edit_message_text(text="No problem, you can come back whenever you want.")
    else:
        query.edit_message_text(
            text="Sorry, I'll do my best the next time :(. I need more images to improve my predictions."
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
    time.sleep(7)

    prediction_result = predict("raw/" + image)
    if prediction_result:
        context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=prediction_result,
            parse_mode="HTML",
            disable_web_page_preview=True,
        )
    reply_markup = keyboard()
    update.message.reply_text("Did I guess your age?", reply_markup=reply_markup)
