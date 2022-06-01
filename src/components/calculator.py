from telegram import InlineKeyboardMarkup, Update, ReplyKeyboardMarkup
from telegram.ext import CallbackContext
from utils.text import button
from src.components import commands
from typing import List


class Calculator():

    @staticmethod
    def __get_currency_rates():
        UZS_TO_USD = 1130090
        USD_TO_UZS = 1145000
        return {
            'uzs-to-usd': UZS_TO_USD,
            'usd-to-uzs': USD_TO_UZS
        }

    @staticmethod
    def __create_default_amounts_markup(
        amounts: List[int], is_dollar: bool,
        header_buttons=None,
        footer_buttons=None
    ) -> ReplyKeyboardMarkup:
        """
        This method builds a markup for currency default amounts
        """

        markup = [amounts[i:i + 2] for i in range(0, len(amounts), 2)]
        if header_buttons:
            markup.insert(0, header_buttons if isinstance(
                header_buttons, list) else [header_buttons])
        if footer_buttons:
            markup.append(footer_buttons if isinstance(
                footer_buttons, list) else [footer_buttons])

        return ReplyKeyboardMarkup(markup, resize_keyboard=True)

    def get_exchange_type(self, update: Update, context: CallbackContext):
        chat_id = update.effective_chat.id
        query = update.callback_query
        query.answer()
        data = query.data
        rates = self.__get_currency_rates()
        query.delete_message()

        # Now, ask to input the amount for calculation.
        # Options for default values are provided.

        if data == 'uzs-to-usd':
            message = "🇺🇿 > 🇺🇸"
            defaults_markup = self.__create_default_amounts_markup(
                [1000, 5000, 10000, 100000, 250000], False,
                footer_buttons=button('back')
            )
        elif data == 'usd-to-uzs':
            message = "🇺🇸 > 🇺🇿"
            defaults_markup = self.__create_default_amounts_markup(
                [1, 5, 10, 200, 100], True, footer_buttons=button('back')
            )
        else:
            commands.Command().invalid_type(update, context)

        context.bot.send_message(chat_id, f"{message}\nOK! Now choose how much you would like to exchange or type in your <b>custom amount</b>",
                                 reply_markup=defaults_markup,
                                 parse_mode='HTML')
        return 'EXCHANGE_OUT'
