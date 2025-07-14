# -*- coding: utf-8 -*-
"""
Created on Thu May 15 21:46:50 2025

@author: kolja
"""
from pathlib import Path
from datetime import datetime
from typing import Literal, List, Annotated, Optional

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import JSONResponse


from pydantic import BaseModel, Field
from pprint import pprint
from lh_core import lock, cache
from lh_portal.dependencies import cache_logs, cache_state, cache_auth
from lh_portal import utils

router = APIRouter(
    prefix="/lock",
    tags=[utils.Tags.lock],
    responses={404: {"description": "Not found"}},
    )

ICON = Literal["locked","closed","open","error","unknown"]

class NukiLog(BaseModel):
    """ Model that represents a SmartlockLog."""
    lock_name: str
    action: str
    state: str
    date: datetime
    date_fmt: str = None

    # error: str = None
    # error_lvl: str = None
    # error_descrition: str = None
    # icon: str = None
    
    @classmethod
    def from_smartlocklog(cls, log: lock.SmartlockLog) -> "NukiLog":
        return cls(lock_name=log.name, 
                   action=log.action.name,
                   state=log.state.name, 
                   date=log.date,
                   date_fmt = utils.date_fmt(log.date))
    
class NukiLogCache(BaseModel):
    """ Cacheinformationen für SmartlockLogs."""
    cache_time: datetime = Field(..., description="Zeitpunkt, zu dem die Nuki-Daten zwischengespeichert wurden.")
    logs: List[NukiLog] = Field(..., description="Liste mit Einträgen von SmartlockLogs.")
    
    @classmethod
    def from_cache(cls, path: Path, limit: int = 5) -> "NukiLogCache":
        dt, data = cache.load_cache(path, lock.SmartlockLogList)
        data = [NukiLog.from_smartlocklog(d) for d in data[:limit]]
        
        return cls(cache_time=dt, logs=data)
        

@router.get("/logs/")
async def nuki_logs(
    path_cache: Annotated[Path, Depends(cache_logs)],
    limit: int = 5
    ) -> NukiLogCache:
    """ get the latest entries of the smartlock logs."""
    data = NukiLogCache.from_cache(path_cache, limit=limit)
    # TODO: check dt and submit update request
    # TODO: setup regular update job.
    return data
    
@router.post("/logs/update/",
             status_code=status.HTTP_202_ACCEPTED,
             responses={202:{"model": utils.AcceptedResponse, "description": "Request submitted to nuki API."}})
async def nuki_logs_cupdate(path_cache: Annotated[Path, Depends(cache_logs)]) -> JSONResponse:
    nuki = lock.Nuki()
    data = nuki.get_logs(lock_id=None, limit=10)
    cache.save_cache(path_cache, data)

    
class NukiState(BaseModel):
    """ Model that represents the current state of the lock."""
    name: str = Field(..., description="Name des Smartlock.")
    state:     str = Field(..., description="Status der Tür (offen, geschlossen, abgeschlossen, unbekannt).") 
    date:      datetime = Field(..., description="Zeitpunkt des Statusupdates.")
    date_fmt:  str = Field(..., description="Formatierter Zeitpunkt des Statusupdates.")
    error:     bool = Field(..., description="Liegt ein Fehler vor.")
    icon:      ICON = Field(..., description="Zu zeigendes Icon.")
        
    @classmethod
    def from_smartlock(cls, smartlock: lock.Smartlock) -> "NukiState":
        
      return cls(name=smartlock.name,
                 state=f"{smartlock.state.state}, {smartlock.state.doorState}",
                 error = smartlock.error or False,
                 icon = "unknown",
                 date = smartlock.updateDate,
                 date_fmt = utils.date_fmt(smartlock.updateDate)
                 )
        
class NukiStateCache(BaseModel):
    cache_time: datetime = Field(..., description="Zeitpunkt, zu dem die Nuki-Daten zwischengespeichert wurden.")
    states: List[NukiState] = Field(..., description="Liste mit Einträgen von Smartlock.")
    
    @classmethod
    def from_cache(cls, path: Path, lock_id: int = None):
        dt, data = cache.load_cache(path, lock.SmartlockList)
        data = [NukiState.from_smartlock(d) for d in data]
        return cls(cache_time=dt, states=data)
    
@router.get("/state/")
async def nuki_state(
    path_cache: Annotated[Path, Depends(cache_state)],
    lock_id: int = None
    ):# -> list[NukiState]:
    """ get the current state of (all) smartlock(s)."""
    data = NukiStateCache.from_cache(path_cache, lock_id=lock_id)
    return data

@router.post("/state/update/",
             status_code=status.HTTP_202_ACCEPTED,
             responses={202:{"model": utils.AcceptedResponse, "description": "Request submitted to nuki API."}})
async def nuki_state_cupdate(path_cache: Annotated[Path, Depends(cache_state)]) -> JSONResponse:
    nuki = lock.Nuki()
    data = nuki.get_smartlock(lock_id=None)
    cache.save_cache(path_cache, data)



class NukiAuth(BaseModel):
    code_name: str
    code: Optional[int] = Field(None, description="Keypad code")
    
    enabled: bool = Field(..., description="Code freigeschaltet?")
    remote: bool  = Field(..., description="Code remote?")
    dt_start: Optional[datetime] = Field(None, description="Startzeit (falls beschränkt)")
    dt_end: Optional[datetime]   = Field(None, description="Endzeit (falls beschränkt)")
    
    @classmethod
    def from_smartlockauth(cls, auth: lock.SmartlockAuth) -> "NukiAuth":
        return cls(
            code_name = auth.name,
            code = auth.code,
            enabled = auth.enabled, remote=auth.remoteAllowed,
            dt_start = auth.allowedFromDate,
            dt_end = auth.allowedUntilDate
            )
    
class NukiAuthCache(BaseModel):
    cache_time: datetime = Field(..., description="Zeitpunkt, zu dem die Nuki-Daten zwischengespeichert wurden.")
    auths: List[NukiAuth] = Field(..., description="Liste mit Einträgen von SmartlockAuths.")
    
    @classmethod
    def from_cache(cls, path: Path):
        dt, data = cache.load_cache(path, lock.SmartlockAuthList)
        auths = [NukiAuth.from_smartlockauth(d) for d in data]
        
        return cls(cache_time=dt, auths=auths)

@router.get("/code/", tags=[utils.Tags.auth])
async def auth_table(
    path_cache: Annotated[Path, Depends(cache_auth)],
    ) -> NukiAuthCache:
    """ get list of all authorisations."""
    data = NukiAuthCache.from_cache(path_cache)
    return data

@router.post("/code/update/", tags=[utils.Tags.auth],
             status_code=status.HTTP_202_ACCEPTED,
             responses={202:{"model": utils.AcceptedResponse, "description": "Request submitted to nuki API."}})
async def nuki_auth_cupdate(path_cache: Annotated[Path, Depends(cache_auth)]) -> JSONResponse:
    nuki = lock.Nuki()
    data = nuki.get_auths(lock_id=None)
    cache.save_cache(path_cache, data)



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


    

@router.post("/action/")
async def lock_action(action: LockAction):
    raise HTTPException(status_code=501, detail="TODO: implement this endpoint")    



@router.post("/code/create", tags=[utils.Tags.auth],)
async def auth_new(request: LockAuthForm):
    raise HTTPException(status_code=501, detail="TODO: implement this endpoint")    

@router.post("/code/update", tags=[utils.Tags.auth],)
async def auth_update(request: LockAuthForm):
    raise HTTPException(status_code=501, detail="TODO: implement this endpoint")    


