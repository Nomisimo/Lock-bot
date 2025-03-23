# -*- coding: utf-8 -*-
"""
Define model representations for the nuki api.

Implemented models:
    - SmartlockLog => LogEntry
    - Smartlock => Smartlock
    - Smartlock.State => SmartlockState
    - SmartlockAuth => SmartlockAuth

@author: kolja
"""
from dataclasses import dataclass, asdict
from datetime import datetime
from enum import Enum

import pytz
from . import const

tz_local = pytz.timezone("Europe/Berlin")
tz_utc = pytz.utc


def dt_to_str(dt: datetime):
    return dt.astimezone(tz_utc).strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3] + 'Z'

def dt_or_none(val: str):
    """ convert to datetime if not None."""
    if isinstance(val, datetime):
        return val
    return (datetime.fromisoformat(val).astimezone(tz_local) 
            if val is not None else None)

def convert_to_json(da: object) -> dict:
    """ convert dataclass back to original json dict."""
    res = asdict(da)
    for k, v in res.items():
        if isinstance(v, Enum):
            res[k] = v.value
        if isinstance(v, datetime):
            res[k] = dt_to_str(v)
    # sort out not set optional values
    res = {k: v for k,v in res.items() if v is not None}
    return res

@dataclass
class LogEntry:
    """ Dataclass modeling the "SmartlockLog"-Model of the API
    """
    id: str
    smartlockId: int
    deviceType: const.DEVICE_TYPE
    name: str
    action: const.ACTION
    trigger: const.TRIGGER
    state: const.LOG_STATE
    autoUnlock: bool
    date: datetime
    
    accountUserid: int = None
    authId: str = None
    openerLog: dict = None      # TODO: handle sub structure
    ajarTimeout: int = None
    source: const.LOG_SOURCE = None
    error: str = None        
    
    
    def __post_init__(self):
        """ handle conversion to Enums/datetime."""
        self.action = const.ACTION(self.action)
        self.deviceType = const.DEVICE_TYPE(self.deviceType)
        self.source = const.LOG_SOURCE(self.source)
        self.state = const.LOG_STATE(self.state)
        self.trigger = const.TRIGGER(self.trigger)
        
        self.date = dt_or_none(self.date)       
    
    def to_json(self):
        """ convert back to json-dict to be send to api."""
        return convert_to_json(self)
    
    @classmethod
    def from_json(cls, data):
        return [cls(**d) for d in data]

    
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





# @dataclass
# class SmartlockAuth:
#     id:             str
#     smartlockId:    str
#     type:           int # ToDo: create const.AUTH_TYPE
#     name:           str
#     enabled:        bool
#     remoteAllowed:  bool
#     lockCount:      int
    
#     accountUserId:  int = None
#     authId:         int = None
#     code:           int = None
#     fingerprints:   dict = None
    
#     allowedFromDate	: datetime = None
#     allowedUntilDate: datetime = None
#     allowedWeekDays:    int = None
#     allowedFromTime	:    int = None
#     allowedUntilTime:   int = None
#     lastActiveDate: datetime = None
#     creationDate:   datetime = None
#     updateDate:     datetime = None
#     operationId:    dict = None
#     error:          str = None
#     appId:          str = None
#     authTypeAsString: str = None
    
    
#     def __post_init__(self):
#         self.type = const.AUTH_TYPE(self.type)
        
#         self.allowedFromDate = dt_or_none(self.allowedFromDate)
#         self.allowedUntilDate = dt_or_none(self.allowedUntilDate)
#         self.creationDate = dt_or_none(self.creationDate)
        
#         self.updateDate = dt_or_none(self.updateDate) 
#         self.lastActiveDate = dt_or_none(self.lastActiveDate)
    
#     def to_json(self):
            
#         res = convert_to_json(self)
#         return res
    