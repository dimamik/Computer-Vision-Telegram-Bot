import datetime
import logging
import os
from pathlib import Path

import telegram
from telegram.ext import CommandHandler
from telegram.ext import MessageHandler, Filters
from telegram.ext import Updater

from ImagesHandler import imageHandler
from var.variables import token

execution_path = os.getcwd().split("\\BotHandler")[0]

bot = telegram.Bot(token=token)
updater = Updater(token=token, use_context=True)
dispatcher = updater.dispatcher

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)


def start(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="Welcome to the Image Bot, please, send me a "
                                                                    "picture")


start_handler = CommandHandler('start', start)
dispatcher.add_handler(start_handler)


def echo(update, context):
    current_date = str(datetime.datetime.now()).split(".")[0].replace(":", "-")
    context.bot.send_message(chat_id=update.effective_chat.id, text="We are working on your image, please wait...")
    Path(execution_path + "\\logs" + f"\\{update.effective_chat.id}").mkdir(parents=True, exist_ok=True)
    file = bot.getFile(update.message.photo[-1].file_id)
    file.download(
        os.path.join(execution_path + "\\logs" + f"\\{update.effective_chat.id}", f'{current_date}.jpg'))

    imageHandler.detect_objects_from_image(
        os.path.join(execution_path + "\\logs" + f"\\{update.effective_chat.id}", f'{current_date}.jpg')
        ,
        os.path.join(execution_path + "\\logs" + f"\\{update.effective_chat.id}",
                     f'{current_date}_new.jpg')
    )
    context.bot.send_photo(chat_id=update.effective_chat.id,
                           photo=open(os.path.join(execution_path + "\\logs" + f"\\{update.effective_chat.id}",
                                                   f'{current_date}_new.jpg'), 'rb'))


echo_handler = MessageHandler(Filters.photo & (~Filters.command), echo)
dispatcher.add_handler(echo_handler)

if __name__ == '__main__':
    updater.start_polling()
