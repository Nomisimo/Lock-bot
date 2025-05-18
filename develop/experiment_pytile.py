# -*- coding: utf-8 -*-
"""
Created on Sun May 18 13:26:17 2025

@author: kolja
"""

from lh_core import config, cache, tracker

from pathlib import Path
import asyncio
from aiohttp import ClientSession
from pytile import async_login
from datetime import datetime
import logging

from pydantic import BaseModel, TypeAdapter
from typing import Literal, TypeVar, List

from pprint import pprint



async def main() -> None:
    """Run!"""
    config.load_config()

    filepath = Path(config.get("portal", "cache")) / "CACHE_tile.json"
    # filepath = tracker.PATH_TRACKER_DEFAULT

    data = await tracker.retrieve_data()    
    cache.save_cache(filepath, data)
    dt, cdata = cache.load_cache(filepath, tracker.CACHE_MODEL)
    
    t1 = data[0]
    t2 = cdata[0]
    print(t1 == t2)
        
# main()
asyncio.run(main())

