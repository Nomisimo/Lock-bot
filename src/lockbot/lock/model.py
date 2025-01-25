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

def convert_to_json(da: object) -> dict:
    """ convert dataclass back to original json dict."""
    res = asdict(da)
    for k, v in res.items():
        if isinstance(v, Enum):
            res[k] = v.value
        if isinstance(v, datetime):
            v = v.astimezone(pytz.utc)
            res[k] = v.strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3] + 'Z'
            
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
        
        self.date = datetime.fromisoformat(self.date).astimezone(tz_local)        
    
    def to_json(self):
        """ convert back to json-dict to be send to api."""
        return convert_to_json(self)
    
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
        self.creationDate = datetime.fromisoformat(self.creationDate)
        self.updateDate = datetime.fromisoformat(self.updateDate)
        
        

    def to_json(self):
        """ convert back to json-dict to be send to api."""
        res = convert_to_json(self)
        res["state"] = convert_to_json(self.state)
        return res
    
    

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
#         self.allowedFromDate = (datetime.fromisoformat(self.allowedFromDate) 
#                                 if self.allowedFromDate is not None else None)
#         self.allowedUntilDate = (datetime.fromisoformat(self.allowedUntilDate) 
#                                  if self.allowedUntilDate is not None else None)
#         self.creationDate = (datetime.fromisoformat(self.creationDate) 
#                              if self.creationDate is not None else None)
#         self.updateDate = (datetime.fromisoformat(self.updateDate) 
#                            if self.updateDate is not None else None)
#         self.lastActiveDate = (datetime.fromisoformat(self.lastActiveDate) 
#                                if self.lastActiveDate is not None else None)
    
#     def to_json(self):
            
#         res = convert_to_json(self)
#         return res
    