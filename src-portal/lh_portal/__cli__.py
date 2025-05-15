# -*- coding: utf-8 -*-
"""
CLI for FastAPI servers

@author: kolja
"""
import argparse
import subprocess
import sys
from pathlib import Path
import logging

def get_main_path():
    path_main = Path(__file__).parent/"__main__.py"
    if not path_main.exists():
        print(f"❌ Datei {path_main} nicht gefunden.")
        sys.exit(1)
    return path_main

def fastapi_dev():
    path_main = get_main_path()
    subprocess.run(["fastapi", "dev", str(path_main)])

def fastapi_run():    
    path_main = get_main_path()
    subprocess.run(["fastapi", "run", str(path_main)])

def main():
    """Main function to load config and start the bot."""
    logging.warning("this is a thin wrapper arround the FastAPI CLI with a set default.")
    parser = argparse.ArgumentParser(
        prog="lh portal",
        description="FastAPI backend for the LautisHannover Portal.", 
        )
    subparsers = parser.add_subparsers(title="command", required=True, help=None)
    
    parser_dev = subparsers.add_parser("dev", help="run in development mode")
    parser_dev.set_defaults(func=fastapi_dev)

    
    parser_run = subparsers.add_parser("run", help="run in development mode")
    parser_run.set_defaults(func=fastapi_run)
    
    args = parser.parse_args()
    args.func()
    

if __name__ == "__main__":
    main()
    