# -*- coding: utf-8 -*-
"""
Created on Thu May 15 21:48:17 2025

@author: kolja
"""

from datetime import datetime
from pathlib import Path
from typing import Annotated

from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse

from pydantic import BaseModel

from lh_core import tracker, cache
from lh_portal.dependencies import cache_tracker


router = APIRouter(
    prefix="/tracker",
    tags=["tracker"],
    responses={404: {"description": "Not found"}},
    )


class TileInfo(BaseModel):
    last_timestamp: datetime
    latitude: float
    longitude: float
    name: str

    @classmethod
    def from_tile_device(cls, device: tracker.TileDevice) -> "TileInfo":
        return cls(**device.model_dump())
    
class TileOverview(BaseModel):
    cache_time: datetime
    tiles: list[TileInfo]


class AcceptedResponse(BaseModel):
    message: str


@router.get("/overview/")
async def tracker_overview(path_cache: Annotated[Path, Depends(cache_tracker)]) -> TileOverview:
    dt, data = cache.load_cache(path_cache, tracker.CACHE_MODEL)
    data = [TileInfo.from_tile_device(d) for d in data]

    # TODO: check dt and submit update request
    # TODO: setup regular update job.
    return TileOverview(cache_time=dt, tiles=data)



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