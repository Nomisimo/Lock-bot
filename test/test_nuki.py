# -*- coding: utf-8 -*-
"""
Created on Mon Jan  6 22:12:08 2025

@author: kolja
"""
import asyncio 
import logging
from lockbot import config
from lockbot import Nuki, AsyncNuki
        
def test():
    logging.info("syncronous")    
    config.load_config()
    nuki = Nuki.new()
    lock_id = nuki.lock_ids[0]
    nuki.post_lock(lock_id)
    print()
    
async def test_async():
    logging.info("async")
    config.load_config()
    nuki = await AsyncNuki.new()
    print()
    
if __name__ == "__main__":
    test()
    # asyncio.run(test_async())
    