# -*- coding: utf-8 -*-
"""
Created on Fri Jan  3 23:35:15 2025

telegram bot with self deleting status message

@author: kolja
"""

from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, filters, MessageHandler


import logging
logging.getLogger("httpx").setLevel(logging.WARNING)

TIME_UPDATE = 10

from lockbot import config

async def handle_start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    # Define the keyboard layout
    keyboard = [
        ["lock", "unlock"],
        ["status", "battery"]
    ]

    # Create a ReplyKeyboardMarkup from the keyboard list
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)

    # Send a message with the keyboard
    await update.message.reply_text(
        'Please choose an option:',
        reply_markup=reply_markup
    )
  
    
from datetime import datetime

async def callback_status(context: ContextTypes.DEFAULT_TYPE):
    chat_id = int(config.get("telegram", "chat_id"))
    msg = f"status: {datetime.now().time()}"
    
    message = await context.bot.send_message(chat_id=chat_id, text=msg)
    context.job_queue.run_once(callback_status_remove, TIME_UPDATE, 
                               data=dict(chat_id=chat_id, message_id=message.message_id))
    
    
async def callback_status_remove(context: ContextTypes.DEFAULT_TYPE):
    data = context.job.data
    await context.bot.delete_message(chat_id=data["chat_id"], message_id=data["message_id"])    


def run_app():
    config.load_config()
    app = ApplicationBuilder().token(config.get("telegram", "api_key")).build()
    app.add_handler(CommandHandler("start", handle_start))
    
    status_job = app.job_queue.run_repeating(callback_status, interval=TIME_UPDATE, first=10)
            
    app.run_polling()

if __name__ == "__main__":
    run_app()