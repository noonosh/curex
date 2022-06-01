from telegram.ext import MessageFilter


class FilterButton():

    def __init__(self, key):
        self.key = key

    def filter(self, message):
        return message.text in ['one', 'two']
