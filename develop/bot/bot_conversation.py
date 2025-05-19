# -*- coding: utf-8 -*-
"""
Created on Tue Mar 25 23:27:50 2025

@author: kolja
"""


import logging
from itertools import batched

from telegram import ReplyKeyboardMarkup, Update, ReplyKeyboardRemove
from telegram.ext import (
    ApplicationBuilder, ConversationHandler,
    ContextTypes, CommandHandler,

)
from lh_core import config

logger = logging.getLogger(__name__)

from collections import defaultdict


def keyboard_from_actions(actions, one_time=False):
    keys = ["/"+key for key in actions]
    
    grid = list(batched(keys, 2))# list(zip(it,it))
    reply_markup = ReplyKeyboardMarkup(grid, resize_keyboard=True, one_time_keyboard=one_time)

    array = [f"- /{key}" for key in actions]
    msg = "\n".join(array)
    return reply_markup, msg


async def handle_not_implemented(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    text = update.message.text
    await update.message.reply_text(f"The action {text} is not implemented.")

ACTIONS = defaultdict(lambda: handle_not_implemented)
ACTIONS["lock"]
ACTIONS["unlock"]
ACTIONS["status"]
ACTIONS["battery"]
ACTIONS["keypad"]
ACTIONS["help"]

async def handle_help(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    markup, msg = keyboard_from_actions(ACTIONS)
    await update.message.reply_text('Choose or type an action:\n'+msg, reply_markup=markup)

ACTIONS["help"] = handle_help


async def handle_start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await handle_help(update, context)
    
    
    
# AUTH = defaultdict(lambda: handle_not_implemented)
# AUTH["create"]
# AUTH["update"]
# AUTH["delete"]
# AUTH["show"]
# AUTH["cancel"]


SELECT, CREATE, UPDATE =  range(3)
AUTH_SELECT = {}
AUTH_CREATE = {} 
AUTH_UPDATE = {}

async def handle_auth_entry(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    # REQUEST AUTHS -> user_data
    actions = list(AUTH_SELECT) + ["cancel"]
    markup, msg = keyboard_from_actions(actions, one_time=False)
    await update.message.reply_text("Select auth action:\n"+msg, reply_markup=markup)
    return SELECT

async def handle_auth_cancel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:    
    logger.info(f"user data:\n{context.user_data}")
    await update.message.reply_text("leaving auth", reply_markup=ReplyKeyboardRemove())
    context.user_data.clear()
    return ConversationHandler.END


async def handle_auth_create(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    # CREATE AUTH with name from args
    context.user_data["auth_action"] = "CREATE"
    actions = list(AUTH_CREATE).appen + ["cancel"]
    markup, msg = keyboard_from_actions(actions, one_time=False)
    await update.message.reply_text("Created auth, modify or submit\n"+msg, reply_markup=markup)
    return CREATE

async def handle_auth_update(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    # SELECT by name from args
    context.user_data["auth_action"] = "UPDATE"
    actions = list(AUTH_UPDATE) + ["cancel"]
    markup, msg = keyboard_from_actions(actions, one_time=False)
    await update.message.reply_text("Update auth, modify or submit\n"+msg, reply_markup=markup)
    return UPDATE

async def handle_auth_show(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    # show all or show name in detail
    await update.message.reply_text("show command")
    return SELECT

async def handle_auth_delete(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    # SELECT and delete from name.
    await update.message.reply_text("delete command")
    return SELECT


async def handle_back_to_select(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    await handle_not_implemented(update, context)
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


def main():
    config.load_config("config_dev.cfg")
    app = ApplicationBuilder().token(config.get("telegram", "api_key")).build()
    app.add_handler(CommandHandler("start", handle_start))

    conv_auth = build_auth_conversation("keypad")
    app.add_handler(conv_auth)


    # add all remaining handlers
    for text, func in (ACTIONS).items():
        if text in ("keypad"):
            continue
        app.add_handler(CommandHandler(text, func))

    # Run the bot until the user presses Ctrl-C
    app.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()