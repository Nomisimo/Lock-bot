# -*- coding: utf-8 -*-
"""
Created on Thu May 15 21:48:17 2025

@author: kolja
"""

from datetime import datetime
from pathlib import Path
from typing import Annotated, List

from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse

from pydantic import BaseModel, Field

from lh_core import tracker, cache
from lh_portal.dependencies import cache_tracker
from lh_portal.utils import AcceptedResponse

router = APIRouter(
    prefix="/tracker",
    tags=["tracker"],
    responses={404: {"description": "Not found"}},
    )


class TileInfo(BaseModel):
    """ Reduzierter Status eines Tile-Trackers."""
    name:        str = Field(..., description="Benutzerdefinierter Name des Tile-Geräts.")
    latitude:  float = Field(..., description="Breitengrad des letzten bekannten Standorts.")
    longitude: float = Field(..., description="Längengrad des letzten bekannten Standorts.")
    last_timestamp: datetime = Field(..., description="Zeitstempel der letzten bekannten Standortdaten.")

    @classmethod
    def from_tile_device(cls, device: tracker.TileDevice) -> "TileInfo":
        return cls(**device.model_dump())
    
class TileCache(BaseModel):
    """ Vollständiges Tracker-Informationspaket."""
    cache_time: datetime = Field(..., description="Zeitpunkt, zu dem die Tile-Daten zwischengespeichert wurden.")
    tiles: List[TileInfo] = Field(..., description="Liste von Tile-Geräten mit grundlegenden Standortinformationen.")

    @classmethod
    def from_cache(path: Path):
         dt, data = cache.load_cache(path, tracker.TileList)
         data = [TileInfo.from_tile_device(d) for d in data]
         return TileCache(cache_time=dt, tiles=data)   


@router.get("/overview/")
async def tracker_overview(path_cache: Annotated[Path, Depends(cache_tracker)]) -> TileCache:
    data = TileCache.from_cache(path_cache)
    # TODO: check dt and submit update request
    # TODO: setup regular update job.
    return data



@router.post("/update/",
             status_code=status.HTTP_202_ACCEPTED,
             responses={202:{"model": AcceptedResponse, "description": "Request submitted to tile server."}})
async def tracker_update(path_cache: Annotated[Path, Depends(cache_tracker)]) -> JSONResponse:
    data = await tracker.retrieve_data()    
    cache.save_cache(path_cache, data)
    return AcceptedResponse(message="Request submitted to tile server.")
    




# from fastapi import FastAPI, BackgroundTasks
# from pydantic import BaseModel

# app = FastAPI()

# class ProcessData(BaseModel):
#     some: str

# @app.post("/process")
# async def process(data: ProcessData):
#     # Simulate some async processing
#     print(f"Processing data: {data.some}")
#     # You could do async IO here (DB calls, external API, etc)
#     return {"status": "processed", "received": data.some}

# @app.post("/trigger")
# async def trigger(background_tasks: BackgroundTasks):
#     # Prepare data to pass to process()
#     data = ProcessData(some="Hello from trigger")
    
#     # Schedule process() as a background task, passing the data
#     background_tasks.add_task(process, data)
    
#     return {"message": "Triggered /process in background"}