# -*- coding: utf-8 -*-
"""
Created on Thu May 15 21:46:50 2025

@author: kolja
"""

from fastapi import APIRouter
from pydantic import BaseModel
from datetime import datetime

router = APIRouter(
    prefix="/lock",
    tags=["lock"],
    responses={404: {"description": "Not found"}},
    )


class LockStatus(BaseModel):
    """ Model that represents the current state of the lock."""
    lock_name: str
    state: str
    date: str
    error: str
    icon: str
        
class LockLog(BaseModel):
    """ Model that represents a SmartlockLog."""
    lock_name: str
    last_action: str
    state: str
    date: str

    error: str = None
    error_lvl: str = None
    error_descrition: str = None
    icon: str = None
    
class LockAction(BaseModel):
    """ Model that represents a action request."""
    lock_name: str
    action: str
    user: str = None
    ip_adress: str = None

class LockAuthForm(BaseModel):
    code_name: str
    dt_start: datetime = None
    dt_stop: datetime = None
    
    user: str = None
    ip_adress: str = None
    created: datetime

class LockAuthEntry(BaseModel):
    code_name: str
    code: int
    
    enabled: bool
    remote: bool
    active: bool
    dt_start: datetime = None
    dt_end: datetime = None
    

@router.get("/preview/")
async def lock_preview() -> list[LockStatus]:
    """ get the current status of (all) smartlock(s)."""
    pass

@router.get("/overview/")
async def lock_overview(limit: int = 5) -> list[LockLog]:
    """ get the latest entries of the smartlock logs."""
    
    pass

@router.post("/action/")
async def lock_action(action: LockAction):
    pass


@router.get("/code/table")
async def auth_table() -> list[LockAuthEntry]:
    pass

@router.post("/code/create")
async def auth_new(request: LockAuthForm):
    pass

@router.post("/code/update")
async def auth_update(request: LockAuthForm):
    pass


