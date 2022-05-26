from telegram import Update
from telegram.ext import CallbackContext
from utils.text import text
import time
import logging


class Starter():

    async def start(self, update: Update, context: CallbackContext):
        chat_id = update.effective_chat.id
        await update.effective_message.reply_text(
            f"Hi, Gay. You are beatiful!!!")
        logging.info("Chat id: %s", chat_id)
        time.sleep(10)
        await update.effective_message.reply_text('timer done')
        return 'state'
