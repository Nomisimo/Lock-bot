# -*- coding: utf-8 -*-
"""
Created on Thu May 15 21:47:53 2025

@author: kolja
"""

from fastapi import APIRouter

router = APIRouter(
    prefix="/power",
    tags=["power"],
    responses={404: {"description": "Not found"}},
    )


@router.get("/overview/")
async def power_overview():
    pass


@router.post("/update/")
async def power_update():
    pass