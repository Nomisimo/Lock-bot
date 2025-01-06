# -*- coding: utf-8 -*-
"""
Created on Sun Jan  5 23:57:33 2025

@author: kolja
"""
import logging

from functools import wraps
from telegram import Update
from telegram.ext import  ContextTypes

from lockbot import config

logger = logging.getLogger(__name__)

def validate_chat_id(func):
    
    @wraps(func)
    async def wrapper(update: Update, context: ContextTypes.DEFAULT_TYPE, *args, **kwargs):
        ALLOWED_IDS = config.get_authorized()
        chat_id = update.effective_chat.id
        if chat_id not in ALLOWED_IDS:
            logger.error(f"Unauthorized access attempt from chat ID {chat_id}.")
            await update.message.reply_text("You are not authorized to use this bot.")
            return
        return await func(update, context, *args, **kwargs)
    return wrapper