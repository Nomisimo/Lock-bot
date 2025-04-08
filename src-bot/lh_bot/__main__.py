# -*- coding: utf-8 -*-
"""
Created on Thu Jan  2 23:06:16 2025

@author: kolja
"""
import os
import argparse
from pathlib import Path
import asyncio
import logging
import getpass


# TODO: move testdata, webhook to other file
from lh_core import config
from lh_bot import create_app


logger = logging.getLogger("lockbot")

def greet():
    """Display a greeting to the user."""
    user = getpass.getuser()  # Ändere hier
    logger.info(f"Hello {user}, lockbot is installed.")

def run_app(path_config: Path, dev: bool=False):
    """ run full app."""
    config.load_config(path=path_config)
    
    app = create_app(token = config.get("telegram", "api_key"),
                      nuki = config.get("nuki", "api_key"),
                      dev = dev
                      )
    app.run_polling()



def main():
    """Main function to load config and start the bot."""
    greet()
    
    parser = argparse.ArgumentParser(
        prog="lockbot",
        description="The LautisHannover smartlock-control-bot.", 
        )
    parser.add_argument("-c", "--config", help="file path of config object", default="config.cfg")
    parser.add_argument("--dev", help="use development mode", action="store_true", default=False)

    parser.set_defaults(func="main")


    args = parser.parse_args()
    path_config = Path(args.config)
    if path_config.is_dir():
        path_config /= "config.cfg"

        
    run_app(path_config, dev=args.dev)
    

if __name__ == "__main__":
    main()
