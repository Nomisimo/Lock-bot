# -*- coding: utf-8 -*-
"""
Created on Mon Mar 10 21:46:52 2025

@author: kolja
"""
import asyncio
import logging
from datetime import datetime

from telegram import Update
from telegram.ext import  ContextTypes

from lockbot import config
from lockbot.bot import auth

logger = logging.getLogger(__name__)


@auth.validate_or_warning()
async def handle_keypad(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """ ToDo: handle keypad dialog
    """
    logger.debug("handle_keypad")
    # nuki = context.bot_data["nuki"]
    # lock_id = context.bot_data["lock_id"]
    # data = await nuki.get_smartlock(lock_id)

    msg = "to be implemented: show all / update / generate keypad codes"
    
    await update.message.reply_text(msg)