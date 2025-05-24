# -*- coding: utf-8 -*-
"""
Created on Thu May 15 21:46:50 2025

@author: kolja
"""
from pathlib import Path
from datetime import datetime
from typing import Literal, List, Annotated

from fastapi import APIRouter, Depends
from pydantic import BaseModel, Field
from pprint import pprint
from lh_core import lock, cache
from lh_portal.dependencies import cache_logs, cache_state

router = APIRouter(
    prefix="/lock",
    tags=["lock"],
    responses={404: {"description": "Not found"}},
    )

ICON = Literal["locked","closed","open","error","unknown"]

class NukiLog(BaseModel):
    """ Model that represents a SmartlockLog."""
    lock_name: str
    action: str
    state: str
    date: datetime

    error: str = None
    error_lvl: str = None
    error_descrition: str = None
    icon: str = None
    
    @classmethod
    def from_smartlocklog(cls, log: lock.SmartlockLog) -> "NukiLog":
        return cls(lock_name=log.name, 
                   action=log.action.name,
                   state=log.state.name, 
                   date=log.date)
        # return cls(lock_name="test",#log.name,
        #            last_action=log.action,
        #            state=log.state,
        #            date=log.date)
    
class NukiLogCache(BaseModel):
    """ Cacheinformationen für SmartlockLogs."""
    cache_time: datetime = Field(..., description="Zeitpunkt, zu dem die Tile-Daten zwischengespeichert wurden.")
    logs: List[NukiLog] = Field(..., description="Liste mit Einträgen von SmartlockLogs.")
    


@router.get("/overview/")
async def lock_overview(
    path_cache: Annotated[Path, Depends(cache_logs)],
    limit: int = 5
    ) -> NukiLogCache:
    """ get the latest entries of the smartlock logs."""
    
    dt, data = cache.load_cache(path_cache, lock.SmartlockLogList)
    pprint(data[0])
    data = [NukiLog.from_smartlocklog(d) for d in data[:3]]
    
    # TODO: check dt and submit update request
    # TODO: setup regular update job.
    return NukiLogCache(cache_time=dt, logs=data)
    
    pass


















class LockStatus(BaseModel):
    """ Model that represents the current state of the lock."""
    name: str = Field(..., description="Name des Smartlock.")
    state:     str = Field(..., description="Status der Tür (offen, geschlossen, abgeschlossen, unbekannt).") 
    date:      str = Field(..., description="Zeitpunkt des Statusupdates.")
    error:     bool = Field(..., description="Liegt ein Fehler vor.")
    icon:      ICON = Field(..., description="Zu zeigendes Icon.")
        
    # @classmethod
    # def from_smartlock(cls, smartlock: lock.Smartlock) -> "LockStatus":
        
    #     state = f"{smartlock.state.state}, {smartlock.state.doorState}"
    #     return cls(lock_name=smartlock.name,
    #                state=state,
    #                date=smartlock.)

    
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


