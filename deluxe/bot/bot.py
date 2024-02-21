from telebot import TeleBot
from telebot.apihelper import ApiTelegramException
import time
import traceback


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



