# -*- coding: utf-8 -*-
"""
Created on Mon Jan  6 22:12:08 2025

@author: kolja
"""
import asyncio 
import logging
from pprint import pprint

from lockbot import config
from lockbot import Nuki, AsyncNuki
from lockbot.lock.model import LogEntry
        
def test():
    logging.info("syncronous")    
    config.load_config("config_dev.cfg")
    nuki = Nuki.new()
    lock_id = nuki.lock_ids[0]
    # nuki.post_lock(lock_id)
    res = nuki.get_logs(lock_id)
    pprint(res)
    
    print()
    

if __name__ == "__main__":
    test()
    