# -*- coding: utf-8 -*-
"""
Created on Thu May 15 20:43:10 2025

@author: kolja
"""

from fastapi import FastAPI
from lh_portal import __version__
from .routers import lock, tracker, power


app = FastAPI(
    title="Lautis API",
    description="This project connects APIs and creates an interface for the management and overview of the systems used by Lautis.",
    version=__version__,
    contact={
        "name": "Lautis Hannover",
        "url": "https://lautis-hannover.de",
        "email": "hallo@lautis-hannover.de",
    },
    license_info={
        "name": "Apache 2.0",
        "url": "https://www.apache.org/licenses/LICENSE-2.0.html",
    },
)

app.include_router(lock.router)
app.include_router(tracker.router)
app.include_router(power.router)

@app.get("/")
async def root():
    return {"message": "Hello World"}


