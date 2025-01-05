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

def main():
    """Main function to load config and start the bot."""
    greet()
    
if __name__ == "__main__":
    main()
