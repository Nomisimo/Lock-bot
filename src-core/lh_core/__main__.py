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


from lh_core import config
from lh_core.tool import testdata, testhook

# TODO: move testdata, webhook to other file
# from lockbot.hook import receiver

logger = logging.getLogger("lockbot")

def greet():
    """Display a greeting to the user."""
    user = getpass.getuser()  # Ändere hier
    logger.info(f"Hello {user}, lockbot is installed.")


def setup_testdata(subparsers):
    """ setup parser for requesting testdata."""
    parser = subparsers.add_parser("testdata", help="generate testdata via API calls.")
    parser.add_argument("-s", "--state", help="generate state data", default=False, action="store_true")
    parser.add_argument("-l", "--logs", help="generate log data", default=False, action="store_true")
    parser.add_argument("-a", "--auths", help="generate auth data", default=False, action="store_true")
    parser.set_defaults(func="testdata")
    return parser
    

def run_testdata(path_config: Path):
    """ request testdata."""
    config.load_config(path=path_config)
    asyncio.run(testdata.generate())
    logger.info("finished, testdata generated.")
    
    
# def setup_testhook(subparsers):
#     """ setup parser for script to send test data to webhook url."""
#     parser = subparsers.add_parser("testhook", help="generate testcalls to webhook.")
#     parser.add_argument("-t", "--time", help="timeout between requests.", type=int)
#     parser.add_argument("-n", "--total", help="number of requests.", type=int)
#     parser.set_defaults(func="testhook")
#     return parser


# def run_testhook(path_config: Path, n=None, timeout=None):
#     """ run script to send testdata to webhook url."""
#     config.load_config(path=path_config)
#     logger.info("started, sending logs to webhook.")
#     n = n or config.get("dev", "testhook_total", fallback=10)
#     timeout = timeout or  config.get("dev", "testhook_timeout", fallback=1)

#     testhook.logger.setLevel(logging.DEBUG)
#     for resp, total, msg in testhook.generate_test_logs():
#         pass
#     logger.info("finished, logs send.")

# def setup_testflask(subparsers):
#     """ setup parser for flask to recieve webhook content."""
#     parser = subparsers.add_parser("testflask", help="run flask to receive webhook calls.")
    
#     parser.set_defaults(func="testflask")
    
# def run_testflask(path_config: Path):
#     """ run flask to recieve data from webhook."""
#     config.load_config(path=path_config)
#     logger.info("starting flask in debug environment")
#     url = config.get("hook", "URL_RECEIVE")
#     host, port = url.split("/")[2].split(":")
#     receiver.app.run(host=host, port=port)

def main():
    """Main function to load config and start the bot."""
    greet()
    
    parser = argparse.ArgumentParser(
        prog="lh tools",
        description="The LautisHannover CLI toolbox.", 
        )
    parser.add_argument("-c", "--config", help="file path of config object", default="config.cfg")

    parser.set_defaults(func="main")

    subparsers = parser.add_subparsers(title="tools", help=None)
    setup_testdata(subparsers)
    # setup_testhook(subparsers)
    # setup_testflask(subparsers)

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
    # if args.func == "testhook":
    #     run_testhook(path_config, n=args.total, timeout=args.time)
    #     return
    # if args.func == "testflask":
    #     run_testflask(path_config)
    #     return
        pass
        
    logger.info("the command was not found")
    

if __name__ == "__main__":
    main()
