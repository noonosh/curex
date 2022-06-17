from telegram import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardRemove, Update, ReplyKeyboardMarkup
from telegram.ext import CallbackContext
from utils.text import text, button, custom
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

    def rate_info(self, update: Update, context: CallbackContext):
        update.effective_message.reply_text("Rate info")

    def exchange(self, update: Update, context: CallbackContext):
        chat_id = update.effective_chat.id

        # Do some cool stuff here...

        m = update.effective_message.reply_text(
            "OK.", reply_markup=ReplyKeyboardRemove())
        context.bot.delete_message(chat_id, message_id=m.message_id)

        update.effective_message.reply_photo(
            photo=open(custom('paths')['choose_exchange_type'], 'rb'),
            caption=text('choose_exchange_type'), parse_mode='HTML', reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton(button('uzs_to_usd'),
                                      callback_data='uzs-to-usd')],
                [InlineKeyboardButton(button('usd_to_uzs'),
                                      callback_data='usd-to-uzs')],
                [InlineKeyboardButton(button('back'),
                                      callback_data='back')]
            ]))

        return 'EXCHANGE_CALCULATOR_TYPE'

    def my_info(self, update: Update, context: CallbackContext):
        update.effective_message.reply_text("Mening ma'lumotlarim menyusi")

    def settings(self, update: Update, context: CallbackContext):
        update.effective_message.reply_text("Sozlamalar menyusi")

    def back_to_display(self, update: Update, context: CallbackContext):

        if update.callback_query:
            query = update.callback_query
            query.answer()
            query.delete_message()

        return self.display(update, context)
