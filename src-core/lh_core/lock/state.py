# -*- coding: utf-8 -*-
"""
Created on Mon Mar 24 21:08:10 2025

@author: kolja
"""

from dataclasses import dataclass
from datetime import datetime

from lh_core.lock import const
from lh_core.lock.utils import convert_to_json, dt_or_none


@dataclass
class SmartlockState:
    """ Dataclass to represent the "Smartlock.State"-model of the API. """
    mode: const.LOCK_MODE
    state: const.LOCK_STATE
    trigger: const.TRIGGER
    lastAction: const.ACTION
    batteryCritical: bool
    
    doorState: const.DOOR_STATE
    nightMode: bool
    
    batteryCharging	: bool = None
    batteryCharge: int = None
    keypadBatteryCritical: bool = None
    doorsensorBatteryCritical: bool = None
    
    ringToOpenTimer: int = None
    ringToOpenEnd: str = None
    operationId: str = None

    def __post_init__(self):
        """ handle conversion to enum."""
        self.mode = const.LOCK_MODE(self.mode)
        self.state = const.LOCK_STATE(self.state)
        self.trigger = const.TRIGGER(self.trigger)
        self.lastAction = const.ACTION(self.lastAction)
        self.doorState = const.DOOR_STATE(self.doorState)
        
    def to_json(self):
        """ convert back to json-dict to be send to api."""
        return convert_to_json(self)

@dataclass
class Smartlock:
    """ Dataclass to represent the "Smartlock"-model of the API."""
    smartlockId:    int
    accountId:      int
    type:           const.DEVICE_TYPE
    
    authId:         int
    name:           str
    favorite:       bool
    serverState:    int
    adminPinState:  int

    config:         dict = None # Smartlock.Config{...}
    advancedConfig: dict = None # Smartlock.AdvancedConfig{...}
    openerAdvancedConfig: dict = None # Smartlock.OpenerAdvancedConfig{...}
    smartdoorAdvancedConfig: dict = None # Smartlock.SmartdoorAdvancedConfig{...}
    webConfig:      dict = None # Smartlock.WebConfig{...}
    state:          SmartlockState = None # Smartlock.State{...}
    
    lmType:             int = None
    firmwareVersion:    int = None
    hardwareVersion:    int = None
    operationId:        str = None
    virtualDevice:      bool = None	      
    creationDate:       datetime = None
    updateDate:         datetime = None
    error:              str = None
    previousSubscriptions:  dict = None # 	ShsSubscription{...}
    currentSubscription:    dict = None 	# ShsSubscription{...}
    region:             int = None
    mountingVariant:    int = None
    opener:             bool = None
    box:                bool = None
    smartDoor:          bool = None
    keyturner:          bool = None

    def __post_init__(self):
        """ convert back to json-dict to be send to api."""
        self.type = const.DEVICE_TYPE(self.type)
        self.state = SmartlockState(**self.state)
        self.creationDate = dt_or_none(self.creationDate)
        self.updateDate = dt_or_none(self.updateDate)
        
        

    def to_json(self):
        """ convert back to json-dict to be send to api."""
        res = convert_to_json(self)
        res["state"] = convert_to_json(self.state)
        return res
    
    @classmethod
    def from_json(cls, data):
        if isinstance(data, list):
            return [cls(**d) for d in data]
        return cls(**data)