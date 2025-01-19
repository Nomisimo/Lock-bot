# -*- coding: utf-8 -*-
"""
Created on Mon Jan  6 13:04:03 2025

@author: kolja
"""
import asyncio

from lockbot import config
from lockbot.lock import request

async def test_status():
    config.load_config()
    astatus = await request.async_get_status()
    status = request.get_status()
    
    print(f"{(status==astatus)=}")
    
async def test_logs():
    config.load_config()
    astatus = await request.async_get_logs()
    status = request.get_logs()

    print(f"{(status==astatus)=}")
        

if __name__ == "__main__":
    asyncio.run(test_status())
    asyncio.run(test_logs())