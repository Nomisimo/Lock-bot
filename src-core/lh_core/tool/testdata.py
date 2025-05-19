# -*- coding: utf-8 -*-
"""
Created on Sat Jan 25 23:43:37 2025

@author: kolja
"""
from pathlib import Path
import asyncio
import json
from time import sleep
import logging

from lh_core import config, cache
from lh_core.lock import AsyncNuki

name_status = "TESTDATA_nuki_state.json"
name_logs =   "TESTDATA_nuki_logs.json"
name_auths =  "TESTDATA_nuki_auths.json"

def path_data(name=None):
    path = config.get_path("dev", "path_data")
    if name:
        path= path.joinpath(name)
    return path

def load_status():
    path_lock = path_data(name_status)
    return cache.load_cache(path_lock, model=None, raw=True)[1]

def load_logfile():
    path_logs = path_data(name_logs)
    return cache.load_cache(path_logs, model=None, raw=True)[1]

def load_auths():
    path_auths = path_data(name_auths)
    return cache.load_cache(path_auths, model=None, raw=True)[1]


async def generate(state: bool=True, 
                   logs: bool=True, 
                   auths: bool = True,
                   ):
    nuki = AsyncNuki()
    lock_id = (await nuki.retrieve_smartlock_ids())[0]
    nuki.set_default_lock()
    assert lock_id
    
    if state:
        # await nuki.post_unlock(lock_id)
        # filepath = path_data(name_unlock)
        # sleep(5)
        # status = await nuki.get_smartlock(lock_id, raw=True)
        # cache.save_cache(filepath, status, raw=True)
        # assert status == cache.load_cache(filepath, model=None, raw=True)[1]
        
        await nuki.post_lock(lock_id)
        filepath = path_data(name_status)
        sleep(5)
        status = await nuki.get_smartlock(lock_id, raw=True)
        cache.save_cache(filepath, status, raw=True)
        assert status == load_status()

    if logs:
        logs = await nuki.get_logs(lock_id, limit=10, raw=True)
        filepath = path_data(name_logs)
        cache.save_cache(filepath, logs, raw=True)
        assert logs == load_logfile()
   
    if auths:
        auths = await nuki.get_auths(lock_id=lock_id, raw=True)
        filepath = path_data(name_auths)
        cache.save_cache(filepath, auths, raw=True)
        assert auths == load_auths()
        
    