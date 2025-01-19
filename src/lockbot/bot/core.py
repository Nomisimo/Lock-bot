# -*- coding: utf-8 -*-
"""
Created on Sun Jan  5 22:27:30 2025

@author: kolja
"""
import logging
from collections import deque
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, filters, MessageHandler

from . import auth
from .action import handle_lock, handle_unlock
from .status import handle_status, handle_battery

from .. import AsyncNuki, config

logger = logging.getLogger(__name__)

ACTIONS = {
    "lock 🔒"   : handle_lock, 
    "unlock 🔓" : handle_unlock,
    "status ❓" : handle_status, 
    "battery 🔋": handle_battery,
    }

    
async def handle_hello(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """ display user id, that has to be added to the config for auth."""
    user = update.effective_user
    await update.message.reply_text(f'Hello {user.username}, {user.id}')

@auth.validate_or_alternative(handle_hello)
async def handle_start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """ Start the bot. Create custom keyboard.    
    """
    await handle_battery(update, context)
    await handle_status(update, context)
    
    # Define the keyboard layout
    it = iter(ACTIONS.keys())
    grid = list(zip(it,it))
    reply_markup = ReplyKeyboardMarkup(grid, resize_keyboard=True)

    # Send a message with the keyboard
    await update.message.reply_text(
        'Choose or type an action:',
        reply_markup=reply_markup
    )
    
async def setup_nuki(app):
    key = app.bot_data["nuki"]
    app.bot_data["nuki"] = await AsyncNuki.new(api_key=key)
    app.bot_data["lock_id"] = config.get("nuki", "lock_id")
    app.bot_data["logs"] = deque(maxlen=10)

def create_app(token: str, nuki: str = None):
    """ Factory function to get the full bot.
    """
    app = ApplicationBuilder().token(token).post_init(setup_nuki).build()
    app.add_handler(CommandHandler("hello", handle_hello))
    app.add_handler(CommandHandler("start", handle_start))
    
    for text, func in ACTIONS.items():
        app.add_handler(MessageHandler(filters.Text(text), func))
        
    app.bot_data["nuki"] = nuki
    logger.info("application created")
    return app