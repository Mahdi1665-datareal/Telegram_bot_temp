from pathlib import Path
import json
import telebot
import os
from loguru import logger
from data import Data_dir
import time
from telebot import types
from src.utils import count_use_decorator, singleton, message_time_decorator, message_lang_detect_decorator


markup = types.ReplyKeyboardMarkup(row_width=2)
list_to_add = ["میخوای کس بگی","کس گفتی","چرت و پرت نگو"]
itembtn_list =list(map(types.KeyboardButton,list_to_add))
markup.add(*itembtn_list)
markup2 = types.ReplyKeyboardRemove(selective=False)

@singleton
class Telegram_bot:
    def __init__(self):
        self.bot = telebot.TeleBot(os.environ['Telegram_bot_token'], parse_mode=None)
        self.send_welcome = self.bot.message_handler(commands=['start', 'help'])(self.send_welcome)
        self.echo_all = self.bot.message_handler(func=lambda message: True)(self.echo_all)
    
    @message_lang_detect_decorator
    @message_time_decorator    
    @count_use_decorator    
    def echo_all(self, message):
        
        if self.echo_all.user_message_count[str(message.from_user.first_name)] == 1:
            self.bot.reply_to(message, " ".join(["جان، شروع کردی به کس  گفتن؟", str(message.from_user.first_name)]))
        else:
            if self.echo_all.detected_lang in ["ur","fa"] :
                self.bot.reply_to(message, " ".join([str(message.from_user.first_name), "Jan, hey tond tond farsi kos begoo ha!"]))
            else:
                self.bot.reply_to(message, " ".join([str(message.from_user.first_name), "Jan, bazam ke ko gofti"]))
        
        if str(message.text) in list_to_add:
            self.bot.send_message(message.chat.id,"Ok", reply_markup=markup2)
        else:
            self.bot.send_message(message.chat.id, "خودت انتخاب کن:", reply_markup=markup)
                
        #with open(Data_dir/ "chat.json", "w") as file:
        #    json.dump(message.json,file, indent=4)
            
    @count_use_decorator    
    def send_welcome(self, message):
        if self.send_welcome.user_message_count[str(message.from_user.first_name)] == 1:
            self.bot.reply_to(message, "this is a bot designed to entertain  Arezou")
        else:
            self.bot.reply_to(message, "Ye bar ke goftam, koskholi chizi hasti?")
        
    
    def Bot_active(self):
        self.bot.infinity_polling()
        logger.info("Telegram bot is running")


if __name__ == "__main__":
    bot_instance = Telegram_bot()
    bot_instance.Bot_active()
