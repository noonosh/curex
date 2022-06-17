import os
import dotenv
import logging
from telegram.ext import (Updater,
                          CommandHandler,
                          ConversationHandler,
                          MessageHandler, Filters,
                          CallbackQueryHandler)
from utils.hide_token import secure_token
from utils.text import open_locale_file, button
from utils.logger import logger
from src.components import start, commands, home, calculator

dotenv.load_dotenv()

# Set Debug to False when in production!
DEBUG = os.environ.get('DEBUG', True)
BOT_TOKEN = os.environ.get('BOT_TOKEN')

start = start.Start()
commands = commands.Commands()
home = home.Home()
calculator = calculator.Calculator()


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
            CommandHandler('start', start.start)
        ],
        states={
            "HOME_DISPLAY": [
                MessageHandler(Filters.regex(button('exchange')),
                               home.exchange),
                MessageHandler(Filters.regex(button('settings')),
                               home.settings),
                MessageHandler(Filters.regex(button('my_info')),
                               home.my_info),
                CommandHandler('kalkulyator', home.exchange),
                CommandHandler('kurs', home.rate_info),
            ],
            "EXCHANGE_CALCULATOR_TYPE": [
                CallbackQueryHandler(
                    calculator.get_exchange_type, pattern='uzs-to-usd|usd-to-uzs'),
                CallbackQueryHandler(
                    home.back_to_display, pattern='back'),
            ],
            "EXCHANGE_AMOUNT": [
                MessageHandler(Filters.regex(button('home_page')),
                               home.back_to_display),
                MessageHandler(Filters.text, calculator.calculate)
            ]
        },
        fallbacks=[
            CommandHandler('help', commands.help),
            CommandHandler('start', commands.start),
            MessageHandler(Filters.text, commands.invalid_type)
        ]
    )

    dispatcher.add_handler(main_conversation)

    updater.start_polling()
    updater.idle()
