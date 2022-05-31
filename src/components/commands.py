from telegram.ext import CallbackContext
from telegram import Update


class Commands():

    def help(self, update: Update, context: CallbackContext):
        """
        Send a friendly message to help to navigate the user in the bot
        """
        update.effective_message.reply_text("Help message")

    def start(self, update: Update, context: CallbackContext):
        update.effective_message.reply_text("Restarted bot")
