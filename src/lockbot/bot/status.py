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
from lockbot.bot import auth
from lockbot.bot.util import remove_job_if_exists, unpin_all
from lockbot.bot import message

logger = logging.getLogger(__name__)


@auth.validate_or_warning()
async def handle_battery(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """ retrieve the smartlock status and send battery info.
    """
    logger.debug("handle_battery")
    nuki = context.bot_data["nuki"]
    lock_id = context.bot_data["lock_id"]
    data = await nuki.get_smartlock(lock_id)
    msg = message.battery(data)
    
    await update.message.reply_text(msg)

async def get_log_from_context(context, n=3):
    nuki = context.bot_data["nuki"]
    lock_id = context.bot_data["lock_id"]
    data = await nuki.get_logs(lock_id, limit=n)
    return data


@auth.validate_or_warning()
async def handle_status(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """ Retrieve logs, show messages for updates and pin the current state at the top.
    """
    logger.debug("handle_status")
    chat_id = update.effective_chat.id
    job_name = f"status_{chat_id}"
    
    # reset status job and pined message
    was_running = remove_job_if_exists(job_name, context)    
    await unpin_all(chat_id, context)
    await asyncio.sleep(0.1)
    if was_running:
        await update.message.reply_text(f"[{message.timestamp()}] status update stopped.")
        return
    else:
        await update.message.reply_text(f"[{message.timestamp()}] status update started.")

    # create pinned message    
    try:
        msg = await update.message.reply_text('status_message')
        await context.bot.pin_chat_message(chat_id=chat_id, message_id=msg.message_id)
    except Exception as e:
        logger.error(f"Error pinning message: {e}")

    # start updates
    interval = int(config.get("telegram", "status_interval", fallback=10))
    context.job_queue.run_repeating(
        update_status_message, 
        interval=interval, first=1, 
        name = job_name, chat_id = update.effective_chat.id,
        data = {"chat_id": update.effective_chat.id, "message_id": msg.message_id}
        )

async def update_status_message(context: ContextTypes.DEFAULT_TYPE) -> None:
    """ Retrieve logs, show messages for updates and pin the current state at the top.
    """
    logger.debug("update_status")
    chat_id = context.job.data["chat_id"]
    message_id = context.job.data["message_id"]
    chat = await context.bot.get_chat(chat_id)

    try:
        # retrieve logs, add to queue and send status messages        
        logs = await get_log_from_context(context, n=3)
        for log in reversed(logs):
            new_text = message.log(log, user=chat.username)
            if log.id in context.bot_data["logs"]:
                continue
            context.bot_data["logs"].append(log.id)
            await context.bot.sendMessage(chat_id, new_text)
        
        # update pinned status message
        if new_text != context.bot_data.get("last_status"):
            await context.bot.edit_message_text(chat_id=chat_id, message_id=message_id, text= new_text)
            context.bot_data["last_status"] = new_text
            
    except Exception as e:
        logger.error(f"Error updating message: ({type(e)}) {e}")
