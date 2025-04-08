# -*- coding: utf-8 -*-
"""
Created on Sun Jan  5 22:27:30 2025

The main module of the telegram bot

@author: kolja
"""
import logging
from collections import deque
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, filters, MessageHandler

from . import auth
from .action import handle_lock, handle_unlock
from .status import handle_status, handle_battery
from .keypad import build_auth_conversation
from .utils import keyboard_from_actions


from lh_core import config
from lh_core.lock import AsyncNuki, DevAsyncNuki

logger = logging.getLogger(__name__)


ACTIONS = {}

@auth.validate_true
async def handle_hello(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """ display user id, that has to be added to the config for auth."""
    user = update.effective_user
    await update.message.reply_text(f'Hello {user.username}, {user.id}')


async def handle_not_implemented(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    text = update.message.text
    await update.message.reply_text(f"The action {text} is not implemented.")

async def handle_help(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    markup, msg = keyboard_from_actions(ACTIONS)
    await update.message.reply_text('Choose or type an action:\n'+msg, reply_markup=markup)

@auth.validate_or_alternative(handle_hello)
async def handle_start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """ Start the bot. Create custom keyboard for actions.    
    """
    # check battery status
    await handle_battery(update, context)
    # start status updates
    await handle_status(update, context)
    
    # display help message
    await handle_help(update, context)
    
    
ACTIONS = {
    "lock"   : handle_lock, 
    "unlock" : handle_unlock,
    "status" : handle_status, 
    "battery": handle_battery,
    "keypad": handle_not_implemented,
    "help": handle_help,
    }
    
async def setup_nuki(app):
    """ setup nuki instance."""
    key = app.bot_data["nuki"]
    if app.bot_data["dev"]:
        app.bot_data["nuki"] = await DevAsyncNuki.new(api_key=key)
    else:
        app.bot_data["nuki"] = await AsyncNuki.new(api_key=key)
        
    app.bot_data["lock_id"] = config.get("nuki", "lock_id")
    app.bot_data["logs"] = deque(maxlen=10)

def create_app(token: str, nuki: str = None, dev: bool=False):
    """ Factory function to create telegram bot.
    """
    app = ApplicationBuilder().token(token).post_init(setup_nuki).build()
    app.add_handler(CommandHandler("hello", handle_hello))
    app.add_handler(CommandHandler("start", handle_start))
    
    conv_auth = build_auth_conversation("keypad")
    app.add_handler(conv_auth)
    
    
    for text, func in ACTIONS.items():
        if text in ("keypad",):
            continue
        app.add_handler(CommandHandler(text, func))
        
    app.bot_data["nuki"] = nuki
    dev = dev  or config.get("nuki", "dev") == "True"
    app.bot_data["dev"] = dev
    logger.info(f"application created ({dev=})")
    return app