# -*- coding: utf-8 -*-
"""
Created on Fri Jan  3 23:35:15 2025

@author: kolja
"""

from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, filters, MessageHandler


import logging
logging.getLogger("httpx").setLevel(logging.WARNING)

TIME_UPDATE = 10

from lockbot import config
from lockbot.config import log_message

from functools import wraps

@wraps
def validate_chat_id(func):
    async def wrapper(update, context, *args, **kwargs):
        ALLOWED_IDS = config.get_authorized()
        print(ALLOWED_IDS)
        chat_id = update.effective_chat.id
        if chat_id not in ALLOWED_IDS:
            log_message(f"Unauthorized access attempt from chat ID {chat_id}.", "security")
            await update.message.reply_text("You are not authorized to use this bot.")
            return
        return await func(update, context, *args, **kwargs)
    return wrapper

async def handle_hello(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user = update.effective_user
    await update.message.reply_text(f'Hello {user.username}, {user.id}')

async def handle_start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text("this should be the door status")

@validate_chat_id
async def handle_secret(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text("this should be secret")



def run_app():
    config.load_config()
    app = ApplicationBuilder().token(config.get("telegram", "api_key")).build()
    app.add_handler(CommandHandler("hello", handle_hello))
    app.add_handler(CommandHandler("start", handle_start))
    app.add_handler(CommandHandler("secret", handle_secret))
    
    # app.add_handler(CommandHandler("status", handle_status))
    # app.add_handler(CommandHandler("battery", handle_battery))
    # app.add_handler(CommandHandler("lock", handle_lock))
    # app.add_handler(CommandHandler("unlock", handle_unlock))
        
    app.run_polling()

if __name__ == "__main__":
    run_app()