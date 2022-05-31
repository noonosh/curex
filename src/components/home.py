from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import CallbackContext
from utils.text import text, button
from ..main import logger


class Home():

    def display(self, update: Update, context: CallbackContext):

        update.effective_message.reply_text(
            text('home_display'),
            reply_markup=ReplyKeyboardMarkup(
                [
                    [button('exchange')],
                    [button('my_info'), button('settings')]
                ],
                resize_keyboard=True))

        logger.info("Home page display for {}".format(
            update.effective_user.id))

        return "HOME_DISPLAY"

    def rate_info(self, update: Update, callback: CallbackContext):
        update.effective_message.reply_text("Rate info")

    def exchange(self, update: Update, callback: CallbackContext):
        update.effective_message.reply_text("Exchange")
