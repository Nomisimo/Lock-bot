# -*- coding: utf-8 -*-
"""
Created on Mon Jan  6 12:27:28 2025

@author: kolja
"""
from pathlib import Path
import asyncio
import json

from lockbot.lock import request
from lockbot import config
from lockbot.lock import parse


path_data = Path("data")
assert path_data.exists(), f"{path_data.resolve()} doesnt exists"
path_lock = path_data.joinpath("data_state_locked.json")
path_unlock = path_data.joinpath("data_state_unlocked.json")
path_logs = path_data.joinpath("data_logs.json")


def testdata_lock():
    return json.loads(path_lock.read_text())    

def testdata_unlock():
    return json.loads(path_unlock.read_text())    

def testdata_logs():
    return json.loads(path_logs.read_text())    

async def generate_testdata():
    config.load_config() 
    await request.async_post_action("lock")
    status = await request.async_get_status()
    path_lock.write_text(json.dumps(status, indent=2))
    assert status == testdata_lock()
    
    await request.async_post_action("unlock")
    status = await request.async_get_status()
    path_unlock.write_text(json.dumps(status, indent=2))
    assert status == testdata_unlock()
    
    logs = await request.async_get_logs(num=5)
    path_logs.write_text((json.dumps(logs,indent=2)))
    assert logs == testdata_logs()
    print("test data saved.")

# if __name__ == "__main__":
#     asyncio.run(generate_testdata())
    

logs = testdata_logs()
ustate = testdata_unlock()
lstate = testdata_lock()
    

parse.state(lstate)

    