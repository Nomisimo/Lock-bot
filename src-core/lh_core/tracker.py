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

from pydantic import BaseModel, TypeAdapter, Field
from typing import Literal, List


class TileDevice(BaseModel):
    uuid: str = Field(..., description="Eindeutige Geräte-ID des Tiles.")
    name: str = Field(..., description="Benutzerdefinierter Name des Geräts.")
    
    accuracy: float = Field(..., description="Genauigkeit der letzten Standortmessung in Metern.")
    altitude: float = Field(..., description="Höhe über dem Meeresspiegel in Metern.")
    latitude: float = Field(..., description="Breitengrad des letzten bekannten Standorts.")
    longitude: float = Field(..., description="Längengrad des letzten bekannten Standorts.")
    last_timestamp: datetime = Field(..., description="Zeitstempel der letzten bekannten Standortdaten.")
    
    kind: Literal["TILE"] = Field(..., description="Typ des Geräts, immer 'TILE'.")
    archetype: str = Field(..., description="Geräte-Archetyp, z. B. 'OTHER', 'KEYS', etc.")
    dead: bool = Field(..., description="Gibt an, ob das Tile als 'verloren' oder 'nicht mehr aktiv' markiert wurde.")
    lost: bool = Field(..., description="Gibt an, ob das Gerät derzeit als verloren markiert ist.")
    visible: bool = Field(..., description="Gibt an, ob das Tile aktuell sichtbar (in Reichweite) ist.")
    lost_timestamp: datetime = Field(..., description="Zeitstempel, wann das Gerät als verloren markiert wurde.")
    
    firmware_version: str = Field(..., description="Firmware-Version des Tile-Geräts.")
    hardware_version: str = Field(..., description="Hardware-Version des Tile-Geräts.")
    ring_state: Literal["STOPPED", "RINGING"] = Field(..., description="Aktueller Klingelzustand des Geräts.")
    voip_state: Literal["OFFLINE", "ONLINE"] = Field(..., description="Aktueller VoIP-Status des Geräts.")


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



async def _example() -> None: # pragma: no cover
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
    assert (t1 == t2), str([t1, t2])
        
# main()
if __name__ == "__main__": # pragma: no cover
    import asyncio
    asyncio.run(_example())

