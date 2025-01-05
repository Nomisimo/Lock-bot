# -*- coding: utf-8 -*-
"""
Created on Thu Jan  2 23:06:16 2025

@author: kolja
"""
import os

from lockbot import config, create_app

def greet():
    """Display a greeting to the user."""
    user = os.getlogin()
    print(f"Hello {user}, lockbot is installed.")

def main():
    """Main function to load config and start the bot."""
    
    config.load_config()
    app = create_app(config.get("telegram", "api_key"))    
    app.run_polling()

if __name__ == "__main__":
    main()
