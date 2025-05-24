# -*- coding: utf-8 -*-
"""
Created on Mon Jan  6 22:12:08 2025

@author: kolja
"""
import logging
from pprint import pprint
from typing import Optional, Union, List

from lh_core import config, cache, lock
# from lh_core import Nuki

def test():
    logging.info("syncronous")    
    config.load_config("config_dev.cfg")
    nuki = lock.Nuki()
    nuki.retrieve_smartlock_ids()
    nuki.set_default_lock()
    
    res = nuki.get_logs(lock_id=None, raw=False, limit=2)
    # res = nuki.get_smartlock(raw=True)
    pprint(res)
    

    

if __name__ == "__main__":
    test()
    