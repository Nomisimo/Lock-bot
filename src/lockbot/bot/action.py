# -*- coding: utf-8 -*-
"""
Created on Sun Jan  5 22:26:20 2025

@author: kolja
"""

from telegram import Update
from telegram.ext import  ContextTypes

async def handle_lock(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """ Send lock action. 
    
    TODO: Implement.
    """
    await update.message.reply_text("this should lock the door")

async def handle_unlock(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """ Send unlock action.
    
    TODO: Implement.
    """
    await update.message.reply_text("this should unlock the door")
   