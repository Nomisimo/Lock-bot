# -*- coding: utf-8 -*-
"""
Created on Tue Mar 25 22:55:40 2025

Develop keypad dialog

@author: kolja
"""
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, filters, MessageHandler, ConversationHandler
from lockbot import config

import logging
logging.getLogger("httpx").setLevel(logging.WARNING)

from datetime import datetime

async def handle_not_implemented(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    text = update.message.text
    await update.message.reply_text(f"The action {text} is not implemented.")

    
    
ACTIONS = {
    "/show" : handle_not_implemented,
    "/create"   : handle_not_implemented, 
    "/update" : handle_not_implemented,
    "/delete" : handle_not_implemented, 
    }

ACTIONS_MOD = {
    "/name": handle_not_implemented,
    "/regen": handle_not_implemented,
    "/status": handle_not_implemented,
    "/time": handle_not_implemented,
    "/reset": handle_not_implemented,
    "/submit": handle_not_implemented,
    }


    

async def handle_start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    # Define the keyboard layout
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
  
    
async def handle_keypad(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    
    pass


def run_app():
    config.load_config("config_dev.cfg")
    app = ApplicationBuilder().token(config.get("telegram", "api_key")).build()
    app.add_handler(CommandHandler("start", handle_start))
    
    for text, func in ACTIONS.items():
        app.add_handler(MessageHandler(filters.Text(text), func))
            
    app.run_polling()

if __name__ == "__main__":
    run_app()