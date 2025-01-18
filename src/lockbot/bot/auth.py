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



def validate_or_warning(warning_text=None):
    """ this decorator replys with a waring msg if the chat is not authorized."""
    
    def decorator(func):
        @wraps(func)
        async def wrapper(update: Update, context: ContextTypes.DEFAULT_TYPE, *args, **kwargs):
            ALLOWED_IDS = config.get_authorized()
            chat_id = update.effective_chat.id
            if chat_id not in ALLOWED_IDS:
                logger.error(f"Unauthorized access attempt from chat ID {chat_id}.")
            
                await update.message.reply_text(warning_text or "You are not authorized to use this bot.")
                return
            return await func(update, context, *args, **kwargs)
        return wrapper    
    return decorator


def validate_or_alternative(alternative_func):
    """ this creates a decorator with an alternative route if the chat is not authorized."""
    
    def decorator(normal_func):
        @wraps(normal_func)
        async def wrapper(update: Update, context: ContextTypes.DEFAULT_TYPE, *args, **kwargs):
            ALLOWED_IDS = config.get_authorized()
            chat_id = update.effective_chat.id

            if chat_id not in ALLOWED_IDS:
                # Log unauthorized access attempt
                logger.error(f"Unauthorized access attempt from chat ID {chat_id}.")
                
                # Run the alternative function as a response
                return await alternative_func(update, context, *args, **kwargs)
            return await normal_func(update, context, *args, **kwargs)
        return wrapper
    return decorator
