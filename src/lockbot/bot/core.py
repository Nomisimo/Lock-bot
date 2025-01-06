# -*- coding: utf-8 -*-
"""
Created on Sun Jan  5 22:27:30 2025

@author: kolja
"""

from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, filters, MessageHandler

from .action import handle_lock, handle_unlock
from .status import handle_status, handle_battery

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

    
async def handle_start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """ Start the bot. Create custom keyboard.
    
    TODO: Autostart status updates.
    TODO: Handle not authorised /start call
    """
    # Define the keyboard layout
    it = iter(ACTIONS.keys())
    grid = list(zip(it,it))
    reply_markup = ReplyKeyboardMarkup(grid, resize_keyboard=True)

    # Send a message with the keyboard
    await update.message.reply_text(
        'Choose or type an action:',
        reply_markup=reply_markup
    )
    

def create_app(token: str):
    """ Factory function to get the full bot.
    """
    app = ApplicationBuilder().token(token).build()
    app.add_handler(CommandHandler("hello", handle_hello))
    app.add_handler(CommandHandler("start", handle_start))
    
    for text, func in ACTIONS.items():
        app.add_handler(MessageHandler(filters.Text(text), func))
    return app