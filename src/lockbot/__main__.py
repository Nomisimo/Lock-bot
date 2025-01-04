# -*- coding: utf-8 -*-
"""
Created on Thu Jan  2 23:06:16 2025

@author: kolja
"""
import os
from lockbot.config import load_config, ConfigError, get
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

def greet():
    """Display a greeting to the user."""
    user = os.getlogin()
    print(f"Hello {user}, lockbot is installed.")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a welcome message when the bot starts."""
    await update.message.reply_text("Hello! Lockbot is ready to manage your lock.")

def main():
    """Main function to load config and start the bot."""
    greet()

    # Load the configuration
    try:
        load_config()  # Load the default config file (config.cfg)
        print("Configuration loaded successfully.")
    except ConfigError as e:
        print(f"Configuration error: {e}")
        return
    except Exception as e:
        print(f"Unexpected error while loading config: {e}")
        return

    # Get Telegram API key from the configuration
    try:
        telegram_api_key = get("telegram", "api_key")
    except ConfigError as e:
        print(f"Error: {e}")
        return

    # Set up and start the Telegram bot
    application = Application.builder().token(telegram_api_key).build()

    # Register command handlers
    application.add_handler(CommandHandler("start", start))

    # Start the bot
    print("Starting Lockbot...")
    application.run_polling()

if __name__ == "__main__":
    main()
