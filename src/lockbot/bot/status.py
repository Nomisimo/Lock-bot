# -*- coding: utf-8 -*-
"""
Created on Sun Jan  5 22:25:46 2025

@author: kolja
"""
import asyncio
import logging
from datetime import datetime

from telegram import Update
from telegram.ext import  ContextTypes

from lockbot import config
from lockbot.bot.util import remove_job_if_exists, unpin_all

logger = logging.getLogger(__name__)


async def handle_battery(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """ retrieve the battery status.
    
    TODO: Implement
    """
    await update.message.reply_text("this should be the battery status, not implemented")


async def handle_status(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """ Retrieve the lock status and display in pinned message.
    
    TODO: Actual retrieve status, format message.
    """
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
        logger.error(f"Error pinning message: {e}")

    interval = int(config.get("telegram", "status_interval", fallback=10))

    # start updates
    context.job_queue.run_repeating(
        update_status_message, 
        interval=interval, first=interval, 
        name = job_name, chat_id = update.effective_chat.id,
        data = {"chat_id": update.effective_chat.id, "message_id": message.message_id}
        )

async def update_status_message(context: ContextTypes.DEFAULT_TYPE) -> None:
    """ Update the status message.
    
    TODO: Actual retrieve the status and format message.
    """
    chat_id = context.job.data["chat_id"]
    message_id = context.job.data["message_id"]
    new_text = f'The lock is closed\n{datetime.now().strftime("%H:%M:%S")}'

    try:
        await context.bot.edit_message_text(chat_id=chat_id, message_id=message_id, text= new_text)
    except Exception as e:
        logger.error(f"Error updating message: {e}")
