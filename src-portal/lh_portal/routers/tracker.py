# -*- coding: utf-8 -*-
"""
Created on Thu May 15 21:48:17 2025

@author: kolja
"""

from fastapi import APIRouter

router = APIRouter(
    prefix="/tracker",
    tags=["tracker"],
    responses={404: {"description": "Not found"}},
    )



@router.get("/overview/")
async def tracker_overview():
    pass


@router.post("/update/")
async def tracker_update():
    pass