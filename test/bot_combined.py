# -*- coding: utf-8 -*-
"""
Created on Sun Jan  5 21:14:23 2025

@author: kolja
"""
from datetime import datetime
import asyncio

from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, filters, MessageHandler
import logging


from lockbot import config
from lockbot.config import log
from lockbot.bot.util import remove_job_if_exists, unpin_all
TIME_UPDATE = 10


async def hello(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(f'Hello {update.effective_user.first_name}')

async def handle_battery(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text("this should be the battery status")

async def handle_lock(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text("this should lock the door")

async def handle_unlock(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text("this should unlock the door")
   
    
async def handle_status(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    chat_id = update.effective_chat.id
    job_name = f"status_{chat_id}"
    
    # reset
    was_running = remove_job_if_exists(job_name, context)    
    await unpin_all(chat_id, context)
    await asyncio.sleep(0.1)
    if was_running:
        await update.message.reply_text("status update stopped.")
        return
    
    # create message
    message = await update.message.reply_text(f'Start time: {datetime.now().strftime("%H:%M:%S")}')
    try:
        await context.bot.pin_chat_message(chat_id=chat_id, message_id=message.message_id)
    except Exception as e:
        log(f"Error pinning message: {e}", "bot", level=logging.ERROR)

    # start updates
    context.job_queue.run_repeating(
        update_status_message, 
        interval=TIME_UPDATE, first=TIME_UPDATE, 
        name = job_name, chat_id = update.effective_chat.id,
        data = {"chat_id": update.effective_chat.id, "message_id": message.message_id}
        )

async def update_status_message(context: ContextTypes.DEFAULT_TYPE) -> None:
    chat_id = context.job.data["chat_id"]
    message_id = context.job.data["message_id"]
    new_text = f'The lock is closed\n{datetime.now().strftime("%H:%M:%S")}'

    try:
        await context.bot.edit_message_text(chat_id=chat_id, message_id=message_id, text= new_text)
    except Exception as e:
        log(f"Error updating message: {e}", "bot", level=logging.ERROR)

    
    
ACTIONS = {
    "lock 🔒"   : handle_lock, 
    "unlock 🔓" : handle_unlock,
    "status ❓" : handle_status, 
    "battery 🔋": handle_battery,
    }
    
    
async def handle_start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    # Define the keyboard layout
    it = iter(ACTIONS.keys())
    grid = list(zip(it,it))
    reply_markup = ReplyKeyboardMarkup(grid, resize_keyboard=True)

    # Send a message with the keyboard
    await update.message.reply_text(
        'Choose or type an action:',
        reply_markup=reply_markup
    )
    

def create_app(token):
    app = ApplicationBuilder().token(token).build()
    app.add_handler(CommandHandler("hello", hello))
    app.add_handler(CommandHandler("start", handle_start))
    
    for text, func in ACTIONS.items():
        app.add_handler(MessageHandler(filters.Text(text), func))
    return app

def run_app():
    config.load_config()
    app = create_app(config.get("telegram", "api_key"))

    
    app.run_polling()

if __name__ == "__main__":
    run_app()