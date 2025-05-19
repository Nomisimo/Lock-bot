# -*- coding: utf-8 -*-
"""
Created on Sun May 18 13:26:17 2025

Load data from the tile tracker api.

@author: kolja, momo
"""

from lh_core import config

from aiohttp import ClientSession
from pytile import async_login
from datetime import datetime
import logging

from pydantic import BaseModel, TypeAdapter
from typing import Literal, List


class TileDevice(BaseModel):
    accuracy: float
    altitude: float
    archetype: str
    dead: bool
    firmware_version: str
    hardware_version: str
    kind: Literal["TILE"]
    last_timestamp: datetime
    latitude: float
    longitude: float
    lost: bool
    lost_timestamp: datetime
    name: str
    ring_state: Literal["STOPPED", "RINGING"]  # je nach API erweitern
    uuid: str
    visible: bool
    voip_state: Literal["OFFLINE", "ONLINE"]  # je nach API erweitern

CACHE_MODEL: BaseModel = TypeAdapter(List[TileDevice])
CACHE_NAME: str = "CACHE_tile.json"


async def retrieve_data():
    logging.debug("starting session")
    async with ClientSession() as session:
        api = await async_login(config.get("tile", "username"), 
                                config.get("tile", "password"), session)
        logging.debug("logged in")
        tiles = await api.async_get_tiles()
        logging.debug("data received")
        data = [TileDevice(**tile.as_dict()) for tile in tiles.values()]
        
    return data



async def _test() -> None:
    """Run!"""
    from pathlib import Path
    from lh_core import cache
    
    
    config.load_config()

    filepath = Path(config.get("portal", "cache")) / "CACHE_tile.json"

    data = await retrieve_data()    
    cache.save_cache(filepath, data)
    dt, cdata = cache.load_cache(filepath, CACHE_MODEL)
    
    t1 = data[0]
    t2 = cdata[0]
    print(t1 == t2)
        
# main()
if __name__ == "__main__":
    import asyncio
    asyncio.run(_test())

