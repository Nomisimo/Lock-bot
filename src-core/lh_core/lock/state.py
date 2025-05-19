# -*- coding: utf-8 -*-
"""
Created on Mon Mar 24 21:08:10 2025

@author: kolja
"""
from datetime import datetime

from pydantic import Field
from typing import Optional

from lh_core.lock import const
from lh_core.lock.utils import NukiModel



class SmartlockState(NukiModel):
    """Pydantic model for the Smartlock.State API response."""

    mode: const.LOCK_MODE = Field(..., description="Der aktuelle Betriebsmodus des Smartlocks.")
    state: const.LOCK_STATE = Field(..., description="Der aktuelle Verriegelungszustand des Smartlocks.")
    doorState: const.DOOR_STATE = Field(..., description="Zustand des Türsensors (falls vorhanden).")
    trigger: const.TRIGGER = Field(..., description="Ursache des letzten Zustandswechsels (z. B. App, Button, AutoUnlock).")
    lastAction: const.ACTION = Field(..., description="Letzte durchgeführte Aktion (z. B. Unlock, Lock, Open).")
    operationId: Optional[str] = Field(None, description="ID der letzten Operation (z. B. Unlock-Vorgang).")
    
    batteryCritical: bool = Field(..., description="Gibt an, ob der Batteriestand kritisch ist.")
    batteryCharging: Optional[bool] = Field(None, description="Gibt an, ob die Batterie derzeit geladen wird.")
    batteryCharge: Optional[int] = Field(None, description="Aktueller Batteriestand in Prozent.")
    keypadBatteryCritical: Optional[bool] = Field(None, description="Kritischer Batteriestand des Keypads.")
    doorsensorBatteryCritical: Optional[bool] = Field(None, description="Kritischer Batteriestand des Türsensors.")

    nightMode: bool = Field(..., description="Gibt an, ob der Nachtmodus aktiviert ist.")
    ringToOpenTimer: Optional[int] = None
    ringToOpenEnd: Optional[str] = None
    
    

class Smartlock(NukiModel):
    """Pydantic model for the Smartlock API object."""

    smartlockId: int
    accountId: int
    type: "const.DEVICE_TYPE"

    authId: int
    name: str
    favorite: bool
    serverState: int
    adminPinState: int

    config: Optional[dict] = None  # Smartlock.Config{...}
    advancedConfig: Optional[dict] = None
    openerAdvancedConfig: Optional[dict] = None
    smartdoorAdvancedConfig: Optional[dict] = None
    webConfig: Optional[dict] = None
    state: Optional["SmartlockState"] = None  # forward reference

    lmType: Optional[int] = None
    firmwareVersion: Optional[int] = None
    hardwareVersion: Optional[int] = None
    operationId: Optional[str] = None
    virtualDevice: Optional[bool] = None
    creationDate: Optional[datetime] = None
    updateDate: Optional[datetime] = None
    error: Optional[str] = None
    previousSubscriptions: Optional[dict] = None  # ShsSubscription{...}
    currentSubscription: Optional[dict] = None    # ShsSubscription{...}
    region: Optional[int] = None
    mountingVariant: Optional[int] = None
    opener: Optional[bool] = None
    box: Optional[bool] = None
    smartDoor: Optional[bool] = None
    keyturner: Optional[bool] = None
    
    
    