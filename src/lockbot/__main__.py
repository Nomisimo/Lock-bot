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


from lockbot import config, create_app
from lockbot.tool import testdata

logger = logging.getLogger("lockbot")

def greet():
    """Display a greeting to the user."""
    user = os.getlogin()
    logger.info(f"Hello {user}, lockbot is installed.")

def run_app(path_config: Path):
    config.load_config(path=path_config)
    
    app = create_app(token = config.get("telegram", "api_key"),
                     nuki= config.get("nuki", "api_key")
                     )
    app.run_polling()
    
def run_testdata(path_config: Path):
    config.load_config(path=path_config)
    asyncio.run(testdata.generate())
    logger.info("finished, testdata generated.")

def main():
    """Main function to load config and start the bot."""
    greet()
    
    parser = argparse.ArgumentParser(
        prog="lockbot",
        description="The LautisHannover smartlock-control-bot.", 
        )
    parser.add_argument("-c", "--config", help="file path of config object", default="config.cfg")
    # parser.add_argument("--testdata", help="generate testdata",
    parser.add_argument("--testdata",  help="generate testdata", default=False, action='store_true')

    args = parser.parse_args()
    path_config = Path(args.config)
    if path_config.is_dir():
        path_config /= "config.cfg"

    if args.testdata:
        run_testdata(path_config)
        return
    
    
    run_app(path_config)
    

if __name__ == "__main__":
    main()
