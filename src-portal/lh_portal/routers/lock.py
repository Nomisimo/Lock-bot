# -*- coding: utf-8 -*-
"""
Created on Thu May 15 21:46:50 2025

@author: kolja
"""

from fastapi import APIRouter

router = APIRouter(
    prefix="/lock",
    tags=["lock"],
    responses={404: {"description": "Not found"}},
    )


@router.get("/preview/")
async def lock_preview():
    pass

@router.get("/overview/")
async def lock_overview():
    pass

@router.post("/action/")
async def lock_action():
    pass


@router.get("/code/table")
async def auth_table():
    pass

@router.post("/code/create")
async def auth_new():
    pass

@router.post("/code/update")
async def auth_update():
    pass


