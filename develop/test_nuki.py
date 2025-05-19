# -*- coding: utf-8 -*-
"""
Created on Mon Jan  6 22:12:08 2025

@author: kolja
"""
import asyncio 
import logging, http
from pprint import pprint
from typing import Optional, Union, List

import httpx

from lh_core import config, cache
from lh_core import Nuki, AsyncNuki
from lh_core.lock import urls, SmartlockLog

from pydantic import parse_obj_as


def test():
    logging.info("syncronous")    
    config.load_config("config_dev.cfg")
    nuki = Nuki()
    nuki.retrieve_smartlock_ids()
    nuki.set_default_lock()
    # nuki.post_lock(lock_id)
    # res = nuki.get_logs(lock_id=None, raw=False, limit=1)
    res = nuki.get_smartlock(raw=True)
    # log = res[2]
    # log2 = SmartlockLog(**log).to_json()
    
    # assert log == (SmartlockLog.from_json(log.to_json()))
    # pprint(res)
    # pprint(log == log2)
    
    

    

if __name__ == "__main__":
    test()
    