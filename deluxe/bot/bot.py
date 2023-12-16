from mongoengine import connect
from telebot import TeleBot
from telebot.apihelper import ApiTelegramException
import time
from config import bot_token, mongourl
import traceback

from deluxe.db import RatingManager
from deluxe.game.ContentManager import ContentManager


class ExtendedBot(TeleBot):
    def send_message(self, *args, **kwargs):
        try:
            return super().send_message(*args, **kwargs)
        except ApiTelegramException as e:
            print(traceback.format_exc())
            if 'Too Many Requests' in e.description:
                time.sleep(5)
                return self.send_message(*args, **kwargs)
        except:
            pass

    def get_deep_link(self, data: str):
        return f"https://t.me/{self.user.username}?start={data}"


bot = ExtendedBot(bot_token, skip_pending=True)
rm = RatingManager()

cm = ContentManager()
connect(host=mongourl, db='viro')
