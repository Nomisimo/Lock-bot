# -*- coding: utf-8 -*-
"""
Created on Mon Jan  6 23:02:15 2025

@author: kolja
"""

from pathlib import Path
import asyncio
import json


from lockbot import config
from lockbot.lock import AsyncNuki


path_data = Path("data")
assert path_data.exists(), f"{path_data.resolve()} doesnt exists"
path_lock = path_data.joinpath("data_state_locked.json")
path_unlock = path_data.joinpath("data_state_unlocked.json")
path_logs = path_data.joinpath("data_logs.json")


def status_locked():
    return json.loads(path_lock.read_text())    

def status_unlocked():
    return json.loads(path_unlock.read_text())    

def logfile():
    return json.loads(path_logs.read_text())    

from time import sleep

async def generate_testdata():
    config.load_config() 
    nuki = await AsyncNuki.new()
    lock_id = nuki.lock_ids[0]
    assert lock_id
    
    await nuki.post_lock(lock_id)
    status = await nuki.get_smartlock(lock_id)
    path_lock.write_text(json.dumps(status, indent=2))
    assert status == status_locked()
    
    sleep(5) #  wait for locking to finish
    
    await nuki.post_unlock(lock_id)
    status = await nuki.get_smartlock(lock_id)
    path_unlock.write_text(json.dumps(status, indent=2))
    assert status == status_unlocked()
    
    sleep(5) # wait for unlocking to finish
    
    logs = await nuki.get_log(lock_id, limit=10)
    path_logs.write_text((json.dumps(logs,indent=2)))
    assert logs == logfile()
    
    print("finished, testdata generated.")

if __name__ == "__main__":
    asyncio.run(generate_testdata())