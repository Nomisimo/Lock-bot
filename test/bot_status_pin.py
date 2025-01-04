# -*- coding: utf-8 -*-
"""
Created on Fri Jan  3 23:35:15 2025

@author: kolja
"""

from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, filters, MessageHandler


import logging
logging.getLogger("httpx").setLevel(logging.WARNING)
logger = logging.getLogger(__name__)
TIME_UPDATE = 10

from lockbot import config
from lockbot.config import log_message
from datetime import datetime


async def handle_start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:

    # unpin all messages
    chat_id = update.effective_chat.id
    try:
        await context.bot.unpin_all_chat_messages(chat_id=chat_id)
        logger.info(f"Unpinned all messages in chat {chat_id}.")
    except Exception as e:
        logger.warning(f"Error unpinning messages in chat {chat_id}: {e}")
    
    # create message
    message = await update.message.reply_text(f'Start time: {datetime.now().strftime("%H:%M:%S")}')
    try:
        await context.bot.pin_chat_message(chat_id=chat_id, message_id=message.message_id)
    except Exception as e:
        log_message(f"Error pinning message: {e}", "error")

    # start updates
    context.job_queue.run_repeating(update_status, 
                                    interval=TIME_UPDATE, first=TIME_UPDATE, 
                                    data = {"chat_id": update.effective_chat.id,
                                            "message_id": message.message_id})

async def update_status(context: ContextTypes.DEFAULT_TYPE) -> None:
    
    chat_id = context.job.data["chat_id"]
    message_id = context.job.data["message_id"]

    try:
        await context.bot.edit_message_text(
            chat_id=chat_id,
            message_id=message_id,
            text=f'The lock is closed\n{datetime.now().strftime("%H:%M:%S")}'
        )
    except Exception as e:
        log_message(f"Error updating message: {e}", "error")



def run_app():
    config.load_config()
    app = ApplicationBuilder().token(config.get("telegram", "api_key")).build()
    app.add_handler(CommandHandler("start", handle_start))
    
            
    app.run_polling()

if __name__ == "__main__":
    run_app()