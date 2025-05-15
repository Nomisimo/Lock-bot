# -*- coding: utf-8 -*-
"""
Created on Thu May 15 20:43:10 2025

@author: kolja
"""

from fastapi import FastAPI

from .routers import lock, tracker, power


app = FastAPI()

app.include_router(lock.router)
app.include_router(tracker.router)
app.include_router(power.router)

@app.get("/")
async def root():
    return {"message": "Hello World"}


