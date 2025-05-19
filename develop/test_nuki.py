# -*- coding: utf-8 -*-
"""
Created on Mon Jan  6 22:12:08 2025

@author: kolja
"""
import asyncio 
import logging
from pprint import pprint

from lh_core import config
from lh_core import Nuki, AsyncNuki
from lh_core.lock import SmartlockLog

        
def test():
    logging.info("syncronous")    
    config.load_config("config_dev.cfg")
    nuki = Nuki.new()
    lock_id = nuki.lock_ids[0]
    # nuki.post_lock(lock_id)
    res = nuki.get_logs(lock_id, raw=True)
    
    log = res[2]
    log2 = SmartlockLog(**log).to_json()
    
    # assert log == (SmartlockLog.from_json(log.to_json()))
    pprint(log)
    pprint(log == log2)
    

if __name__ == "__main__":
    test()
    