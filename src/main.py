from commands import button, help_command, photo, start, text, unknown
from config.settings import BOT_TELEGRAM_TOKEN
from errors import error_handler
from telegram.ext import (
    CallbackQueryHandler,
    CommandHandler,
    Filters,
    MessageHandler,
    Updater,
)
from utils.logging import telegram_bot


def main():
    """
    Main function to declare the dispacther, command handlers and message handlers.
    This function poll the updates from telegram with a polling.
    - Commands:
        - /start -> Start the bot.
        - /help -> Get the help.
        - /whatever -> Unknown command.
    - MessageHandler:
        - Photos -> These are required.
        - Gifs, Videos, Text, etc -> Not allowed
    """
    telegram_bot.info("Starting telegram bot.")
    updater = Updater(BOT_TELEGRAM_TOKEN, use_context=True, workers=32)

    dispatcher = updater.dispatcher
    dispatcher.add_error_handler(error_handler)

    dispatcher.add_handler(CommandHandler("start", start))

    dispatcher.add_handler(
        MessageHandler(Filters.photo & ~Filters.command, photo, run_async=True)
    )

    text_handler = MessageHandler(
        Filters.text & (~Filters.command), text, run_async=True
    )
    dispatcher.add_handler(text_handler)

    dispatcher.add_handler(CommandHandler("help", help_command))

    updater.dispatcher.add_handler(CallbackQueryHandler(button))

    unknown_handler = MessageHandler(Filters.command, unknown, run_async=True)
    dispatcher.add_handler(unknown_handler)

    telegram_bot.info("Start polling.")

    updater.start_polling()
    updater.idle()


if __name__ == "__main__":
    main()
