import os
import dotenv
import logging
from telegram.ext import (Updater,
                          CommandHandler,
                          ConversationHandler,
                          MessageHandler, Filters)
from utils.hide_token import secure_token
from utils.text import open_locale_file, button
from utils.logger import logger
from src.components import start, commands, home

dotenv.load_dotenv()

# Set Debug to False when in production!
DEBUG = os.environ.get('DEBUG', True)
BOT_TOKEN = os.environ.get('BOT_TOKEN')

starter = start.Starter()
command = commands.Commands()
home = home.Home()


def main():
    updater = Updater(BOT_TOKEN)
    dispatcher = updater.dispatcher
    logger.debug(
        f"Bot instance {secure_token(BOT_TOKEN)} has been initialized. Dispatcher set!")

    try:
        open_locale_file()
        logger.debug("Locale file has successfully worked, texts are ready.")
    except Exception as e:
        logger.error(f"Error opening locale file: {e}")

    main_conversation = ConversationHandler(
        entry_points=[
            CommandHandler('start', starter.start)
        ],
        states={
            "HOME_DISPLAY": [
                MessageHandler(Filters.text(button('exchange')),
                               home.exchange),
                CommandHandler('kalkulyator', home.exchange),
                CommandHandler('kurs', home.rate_info),
            ]
        },
        fallbacks=[
            CommandHandler('help', command.help),
            CommandHandler('start', command.start)
        ]
    )

    dispatcher.add_handler(main_conversation)

    updater.start_polling()
    updater.idle()
