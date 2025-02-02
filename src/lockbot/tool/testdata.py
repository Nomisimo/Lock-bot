# -*- coding: utf-8 -*-
"""
Created on Sat Jan 25 23:43:37 2025

@author: kolja
"""
from pathlib import Path
import asyncio
import json
from time import sleep


from lockbot import config
from lockbot.lock import AsyncNuki

name_lock = "data_state_locked.json"
name_unlock = "data_state_unlocked.json"
name_logs = "data_logs.json"
name_auths = "data_auths.json"

def path_data(name=None):
    path = config.get_path("dev", "path_data")
    if name:
        path= path.joinpath(name)
    return path

def load_status(version="lock"):
    names = dict(lock=name_lock, unlock=name_unlock)
    path_lock = path_data(names[version])
    return json.loads(path_lock.read_text())    

def load_logfile():
    path_logs = path_data(name_logs)
    return json.loads(path_logs.read_text())    

def load_auths():
    path_auths = path_data(name_auths)
    return json.loads(path_auths.read_text())


async def generate(state: bool=True, logs: bool=True, auths: bool = True):
    nuki = await AsyncNuki.new()
    lock_id = nuki.lock_ids[0]
    assert lock_id
    
    
    if state:
        await nuki.post_lock(lock_id)
        status = await nuki.get_smartlock(lock_id, raw=True)
        path_data(name_lock).write_text(json.dumps(status, indent=2))
        assert status == load_status("lock")
        print(path_data(name_lock))
        sleep(5) #  wait for locking to finish
        
        await nuki.post_unlock(lock_id)
        status = await nuki.get_smartlock(lock_id, raw=True)
        path_data(name_unlock).write_text(json.dumps(status, indent=2))
        assert status == load_status("unlock")
        print(path_data(name_unlock))
        sleep(5) # wait for unlocking to finish
    
    if logs:
        logs = await nuki.get_logs(lock_id, limit=100, raw=True)
        path_data(name_logs).write_text((json.dumps(logs,indent=2)))
        assert logs == load_logfile()
        print(path_data(name_logs))
    
    if auths:
        data = await nuki.get_auth(raw=True)
        path_data(name_auths).write_text(json.dumps(data, indent=2))
        assert data == load_auths()
        print(path_data(name_auths))
    
    
    