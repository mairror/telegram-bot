from telegram.ext import (
    Updater, 
    CommandHandler, 
    MessageHandler, 
    Filters
)
from utils.logging import telegram_bot
from config.settings import BOT_TELEGRAM_TOKEN
from commands import start, photo, text, help_command, unknown



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
    updater = Updater(
        BOT_TELEGRAM_TOKEN,
        use_context=True,
        workers=32)

    dispatcher = updater.dispatcher
    
    dispatcher.add_handler(CommandHandler("start", start))
    
    dispatcher.add_handler(MessageHandler(Filters.photo & ~Filters.command, photo, run_async=True))
    
    text_handler = MessageHandler(Filters.text & (~Filters.command), text, run_async=True)
    dispatcher.add_handler(text_handler)
    
    dispatcher.add_handler(CommandHandler("help", help_command))
    
    unknown_handler = MessageHandler(Filters.command, unknown, run_async=True)
    dispatcher.add_handler(unknown_handler)


    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()

