from telebot import TeleBot
from telebot.apihelper import ApiTelegramException
import time
from config import bot_token
import traceback


class ExtendedBot(TeleBot):
    def send_message(self, *args, **kwargs):
        try:
            super().send_message(*args, **kwargs)
        except ApiTelegramException as e:
            print(traceback.format_exc())
            if 'Too Many Requests' in e.description:
                time.sleep(2)
                self.send_message(*args, **kwargs)


bot = TeleBot(bot_token)
