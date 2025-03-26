# -*- coding: utf-8 -*-
"""
Created on Tue Mar 25 23:27:50 2025

@author: kolja
"""


import logging

from telegram import ReplyKeyboardMarkup, Update
from telegram.ext import (
    ApplicationBuilder,
    ContextTypes, CommandHandler,
    MessageHandler,
    filters,
)
from lockbot import config

logger = logging.getLogger(__name__)

from collections import defaultdict

async def handle_not_implemented(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    text = update.message.text
    await update.message.reply_text(f"The action {text} is not implemented.")

ACTIONS = defaultdict(lambda: handle_not_implemented)
ACTIONS["/lock"]
ACTIONS["/unlock"]
ACTIONS["/status"]
ACTIONS["/battery"]
ACTIONS["/keypad"]
ACTIONS["/help"]

async def handle_help(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    
    # Define the keyboard layout
    it = iter(ACTIONS.keys())
    grid = list(zip(it,it))
    reply_markup = ReplyKeyboardMarkup(grid, resize_keyboard=True)

    array = [f"- {key}" for key in ACTIONS.keys()]

    # Send a message with the keyboard
    await update.message.reply_text(
        'Choose or type an action:\n'+"\n".join(array),
        reply_markup=reply_markup
    )
ACTIONS["/help"] = handle_help


async def handle_start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await handle_help(update, context)
    
    



def main():
    config.load_config("config_dev.cfg")
    app = ApplicationBuilder().token(config.get("telegram", "api_key")).build()
    app.add_handler(CommandHandler("start", handle_start))
    for text, func in ACTIONS.items():
        # app.add_handler(CommandHandler(text, func))
        app.add_handler(MessageHandler(filters.Text(text), func))
    

    # Run the bot until the user presses Ctrl-C
    app.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()