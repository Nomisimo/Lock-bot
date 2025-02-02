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
from lockbot.tool import testdata, testhook

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


def setup_testdata(subparsers):
    parser = subparsers.add_parser("testdata", help="generate testdata via API calls.")
    parser.add_argument("-s", "--state", help="generate state data", default=False, action="store_true")
    parser.add_argument("-l", "--logs", help="generate log data", default=False, action="store_true")
    parser.add_argument("-a", "--auths", help="generate auth data", default=False, action="store_true")
    parser.set_defaults(func="testdata")
    return parser
    

def run_testdata(path_config: Path):
    config.load_config(path=path_config)
    asyncio.run(testdata.generate())
    logger.info("finished, testdata generated.")
    
    
def setup_testhook(subparsers):
    parser = subparsers.add_parser("testhook", help="generate testcalls to webhook.")
    parser.add_argument("-t", "--time", help="timeout between requests.", type=int)
    parser.add_argument("-n", "--total", help="number of requests.", type=int)
    parser.set_defaults(func="testhook")
    return parser


def run_testhook(path_config: Path, n=None, timeout=None):
    config.load_config(path=path_config)
    logger.info("started, sending logs to webhook.")
    n = n or config.get("dev", "testhook_total", fallback=10)
    timeout = timeout or  config.get("dev", "testhook_timeout", fallback=1)

    testhook.logger.setLevel(logging.DEBUG)
    for resp, total, msg in testhook.generate_test_logs():
        pass
    logger.info("finished, logs send.")

def main():
    """Main function to load config and start the bot."""
    greet()
    
    parser = argparse.ArgumentParser(
        prog="lockbot",
        description="The LautisHannover smartlock-control-bot.", 
        )
    parser.add_argument("-c", "--config", help="file path of config object", default="config.cfg")
    parser.set_defaults(func="main")

    subparsers = parser.add_subparsers(title="tools", help=None)
    setup_testdata(subparsers)
    setup_testhook(subparsers)

    args = parser.parse_args()
    
    path_config = Path(args.config)
    if path_config.is_dir():
        path_config /= "config.cfg"

    if args.func == "testdata":
        if any([args.state, args.logs, args.auths]):
            run_testdata(path_config, state=args.state, logs=args.logs, auths=args.auths)
        else:
            run_testdata(path_config)
            
        return
    if args.func == "testhook":
        print(args)
        run_testhook(path_config, n=args.total, timeout=args.time)
        return
    
    run_app(path_config)
    

if __name__ == "__main__":
    main()
