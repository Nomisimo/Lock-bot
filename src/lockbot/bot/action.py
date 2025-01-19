# -*- coding: utf-8 -*-
"""
Created on Sun Jan  5 22:26:20 2025

@author: kolja
"""
import logging
logger = logging.getLogger(__name__)

from telegram import Update
from telegram.ext import  ContextTypes

from lockbot.bot import auth


@auth.validate_or_warning()
async def handle_lock(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """ Send lock action. 
    """
    logger.debug("handle_lock")
    nuki = context.bot_data["nuki"]
    lock_id = context.bot_data["lock_id"]
    success = await nuki.post_lock(lock_id)
    
    await update.message.reply_text("door should lock")

@auth.validate_or_warning()
async def handle_unlock(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """ Send unlock action.
    """
    logger.debug("handle_lock")
    nuki = context.bot_data["nuki"]
    lock_id = context.bot_data["lock_id"]
    success = await nuki.post_unlock(lock_id)
    
    await update.message.reply_text("door should unlock")

