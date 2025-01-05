# -*- coding: utf-8 -*-
"""
Created on Fri Jan  3 23:35:15 2025

@author: kolja
"""

from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, filters, MessageHandler


import logging
# logging.getLogger("httpx").setLevel(logging.WARNING)
# logger = logging.getLogger(__name__)
TIME_UPDATE = 10

from lockbot import config
from lockbot.config import log
from datetime import datetime

import asyncio 
LOCK_STATUS = None

def remove_job_if_exists(name: str, context: ContextTypes.DEFAULT_TYPE) -> bool:
    """Remove job with given name. Returns whether job was removed."""
    current_jobs = context.job_queue.get_jobs_by_name(name)
    if not current_jobs:
        return False
    for job in current_jobs:
        job.schedule_removal()
    return True

async def unpin_all(chat_id: int, context: ContextTypes.DEFAULT_TYPE):
    try:
        await context.bot.unpin_all_chat_messages(chat_id=chat_id)
        log(f"Unpinned all messages in chat {chat_id}.", "bot")
    except Exception as e:
        log(f"Error unpinning messages in chat {chat_id}: {e}", "bot", logging.ERROR)
    

async def handle_start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    chat_id = update.effective_chat.id
    job_name = f"status_{chat_id}"
    remove_job_if_exists(job_name, context)    
    await unpin_all(chat_id, context)
    await asyncio.sleep(0.1)
    
    # create message
    message = await update.message.reply_text(f'Start time: {datetime.now().strftime("%H:%M:%S")}')
    try:
        await context.bot.pin_chat_message(chat_id=chat_id, message_id=message.message_id)
    except Exception as e:
        log(f"Error pinning message: {e}", "bot", level=logging.ERROR)

    # start updates
    context.job_queue.run_repeating(update_message, 
                                    interval=TIME_UPDATE, first=TIME_UPDATE, 
                                    name = job_name,
                                    chat_id = update.effective_chat.id,
                                    data = {"chat_id": update.effective_chat.id,
                                            "message_id": message.message_id})

async def update_message(context: ContextTypes.DEFAULT_TYPE) -> None:
    
    chat_id = context.job.data["chat_id"]
    message_id = context.job.data["message_id"]

    try:
        await context.bot.edit_message_text(
            chat_id=chat_id,
            message_id=message_id,
            text=f'The lock is closed\n{datetime.now().strftime("%H:%M:%S")}'
        )
    except Exception as e:
        log(f"Error updating message: {e}", "bot", level=logging.ERROR)



def run_app():
    config.load_config()
    app = ApplicationBuilder().token(config.get("telegram", "api_key")).build()
    app.add_handler(CommandHandler("start", handle_start))
    
            
    app.run_polling()

if __name__ == "__main__":
    run_app()