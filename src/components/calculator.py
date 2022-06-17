from telegram import InlineKeyboardMarkup, Update, ReplyKeyboardMarkup
from telegram.ext import CallbackContext
from utils.text import button, text
from utils.misc import format_currency
from src.components import commands
from typing import List
import requests
from bs4 import BeautifulSoup
import html
import re


class Calculator():

    @staticmethod
    def __get_currency_rates():
        # URL to fetch to get the data from
        URL = 'https://bank.uz/currency/dollar-ssha'

        # Make a GET request
        res = requests.get(URL)

        html_doc = html.unescape(res.text)
        soup = BeautifulSoup(html_doc, 'html.parser')

        # Not a typo. 'curs' shorthand for currencies
        curs = soup.find_all('div', class_='col-4')
        print(type(curs))

        UZS_TO_USD = 11450.01
        USD_TO_UZS = 11300.00

        return {
            'uzs-to-usd': UZS_TO_USD,
            'usd-to-uzs': USD_TO_UZS
        }

    @staticmethod
    def __create_default_amounts_markup(
        self,
        amounts: List[int], is_dollar: bool,
        header_buttons=None,
        footer_buttons=None
    ) -> ReplyKeyboardMarkup:
        """
        This method builds a markup for currency default amounts
        """
        amounts = [
            f'${format_currency(amount)}' if is_dollar else f'{format_currency(amount)} UZS' for amount in amounts]

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
        query.delete_message()
        context.user_data.update({
            "user_id": chat_id,
            "operation": data
        })

        # Now, ask to input the amount for calculation.
        # Options for default values are provided.

        if data == 'uzs-to-usd':
            message = "🇺🇿 ➡️ 🇺🇸"
            defaults_markup = self.__create_default_amounts_markup(
                self,
                [1000, 5000, 10000, 100000, 250000], False,
                footer_buttons=button('home_page')
            )
        elif data == 'usd-to-uzs':
            message = "🇺🇸 ➡️ 🇺🇿"
            defaults_markup = self.__create_default_amounts_markup(
                self,
                [1, 5, 10, 200, 100000], True,
                footer_buttons=button('home_page')
            )
        else:
            commands.Command().invalid_type(update, context)

        context.bot.send_message(chat_id, message + '\n\n' + text('choose_or_input_amount'),
                                 reply_markup=defaults_markup,
                                 parse_mode='HTML')
        return 'EXCHANGE_AMOUNT'

    def calculate(self, update: Update, context: CallbackContext):
        chat_id = update.effective_chat.id
        message = update.effective_message.text

        rates = self.__get_currency_rates()
        operation = context.user_data['operation']

        # Convert the number format for further processing
        amount = float(re.findall(
            r'[\d\.\,\d]+', message)[0].replace(',', ''))

        # TODO: Using a symbol to represent the currency
        if operation == 'uzs-to-usd':
            out = amount / rates[operation]
            symbol = "$"
        elif operation == 'usd-to-uzs':
            out = rates[operation] * amount
            symbol = " UZS"
        else:
            commands.Command().invalid_type(update, context)

        out_text = text('calculator_out').format("{:,.2f}".format(out))

        context.bot.send_message(chat_id, out_text, parse_mode='HTML')
