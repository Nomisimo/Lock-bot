# -*- coding: utf-8 -*-
"""
Created on Mon Mar 10 21:46:52 2025

Generate and update codes for the keypad.

@author: kolja
"""
import asyncio
import logging
from datetime import datetime
from itertools import batched

from telegram import ReplyKeyboardMarkup, Update, ReplyKeyboardRemove
from telegram.ext import (
    ConversationHandler,
    ContextTypes, CommandHandler,

)
from lockbot import config
from lockbot.bot import auth
from lockbot.bot.utils import keyboard_from_actions
from lockbot.bot import message

logger = logging.getLogger(__name__)



SELECT, CREATE, UPDATE =  range(3)
AUTH_SELECT = {}
AUTH_CREATE = {} 
AUTH_UPDATE = {}

async def update_auths_cache(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    nuki = context.bot_data["nuki"]
    lock_id = context.bot_data["lock_id"]
    context.user_data["AUTHS"] = await nuki.get_auth(lock_id)  

@auth.validate_or_warning()
async def handle_auth_entry(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    # REQUEST AUTHS -> user_data
    logger.debug("handle_auth_entry")
    await update_auths_cache(update, context)
    
    # show options
    actions = list(AUTH_SELECT) + ["cancel"]
    markup, msg = keyboard_from_actions(actions, one_time=False)
    await update.message.reply_text("Select auth action:\n"+msg, reply_markup=markup)
    return SELECT

async def handle_auth_cancel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:    
    logger.debug("handle_auth_cancel")
    logger.info(f"user data:\n{context.user_data}")
    await update.message.reply_text("leaving auth", reply_markup=ReplyKeyboardRemove())
    context.user_data.clear()
    return ConversationHandler.END

async def handle_auth_create(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    # CREATE AUTH with name from args
    logger.debug("handle_auth_create")
    context.user_data["auth_action"] = "CREATE"
    actions = list(AUTH_CREATE) + ["cancel"]
    markup, msg = keyboard_from_actions(actions, one_time=False)
    await update.message.reply_text("Created auth, modify or submit\n"+msg, reply_markup=markup)
    return CREATE

async def handle_auth_update(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    # SELECT by name from args
    logger.debug("handle_auth_update")
    
    context.user_data["auth_action"] = "UPDATE"
    actions = list(AUTH_UPDATE) + ["cancel"]
    markup, msg = keyboard_from_actions(actions, one_time=False)
    await update.message.reply_text("Update auth, modify or submit\n"+msg, reply_markup=markup)
    return UPDATE

async def handle_auth_show(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    logger.debug("handle_auth_show")
    
    await update_auths_cache(update, context)
    
    if len(context.args) == 0:
        # show all names
        msg = message.auth_show_all(context.user_data["AUTHS"])
    elif "help" in context.args:
        msg = message.auth_show_help()
    else:
        name = " ".join(context.args)
        AUTHS = context.user_data["AUTHS"]
        auth = AUTHS.by_name(name).selected()
        msg = message.auth_show(auth)
        AUTHS.reset_selection()

    await update.message.reply_text(msg)
    return SELECT

async def handle_auth_delete(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    logger.debug("handle_auth_show")
    

    if len(context.args) == 0 or "help" in context.args:
        msg = message.auth_del_help()
        await update.message.reply_text(msg)
        return SELECT

    await update_auths_cache(update, context)
    nuki = context.bot_data["nuki"]
    auths = context.user_data["AUTHS"]
    name = " ".join(context.args)
    selected = auths.delete(name)
    val = await nuki.del_auth(selected)
    if val:
        msg = message.auth_del_success(selected)
    else:
        msg = message.auth_del_fail(selected)
    await update.message.reply_text(msg)

    return SELECT


async def handle_back_to_select(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    text = update.message.text
    await update.message.reply_text(f"The action {text} is not implemented.")
    return SELECT


AUTH_SELECT = {
    "create": handle_auth_create,
    "update": handle_auth_update,
    "show": handle_auth_show,
    "delete": handle_auth_delete,
    }

AUTH_CREATE = {
    "name" : handle_back_to_select,
    "code" : handle_back_to_select,
    "enable" : handle_back_to_select,
    "time" : handle_back_to_select,
    "submit" : handle_back_to_select,
    }    
AUTH_UPDATE = AUTH_CREATE

def build_auth_conversation(entry: str = "keypad"):
    keypad_conversation = ConversationHandler(
        entry_points=[CommandHandler(entry, handle_auth_entry)],
        fallbacks=[CommandHandler("cancel", handle_auth_cancel)],
        states = {
            SELECT: [CommandHandler(name, func) for name, func in AUTH_SELECT.items()],
            CREATE: [CommandHandler(name, func) for name, func in AUTH_CREATE.items()],
            UPDATE: [CommandHandler(name, func) for name, func in AUTH_UPDATE.items()],
            },
        )
    return keypad_conversation
