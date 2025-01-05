# -*- coding: utf-8 -*-
"""
Created on Fri Jan  3 23:35:15 2025

@author: kolja
"""

from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, filters, MessageHandler


import logging

TIME_UPDATE = 10

from lockbot import config
from lockbot.config import log

async def hello(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(f'Hello {update.effective_user.first_name}')

async def handle_status(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text("this should be the door status")

async def handle_battery(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text("this should be the battery status")

async def handle_lock(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text("this should lock the door")

async def handle_unlock(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text("this should unlock the door")
    
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
  
  
def run_app():
    config.load_config()
    app = ApplicationBuilder().token(config.get("telegram", "api_key")).build()
    app.add_handler(CommandHandler("hello", hello))
    app.add_handler(CommandHandler("start", handle_start))
    
    # app.add_handler(CommandHandler("status", handle_status))
    # app.add_handler(CommandHandler("battery", handle_battery))
    # app.add_handler(CommandHandler("lock", handle_lock))
    # app.add_handler(CommandHandler("unlock", handle_unlock))
    
    app.add_handler(MessageHandler(filters.Text("status"), handle_status))
    app.add_handler(MessageHandler(filters.Text("lock"), handle_lock))
    app.add_handler(MessageHandler(filters.Text("unlock"), handle_unlock))
    app.add_handler(MessageHandler(filters.Text("battery"), handle_battery))
    
    app.run_polling()

if __name__ == "__main__":
    run_app()