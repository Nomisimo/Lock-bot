# -*- coding: utf-8 -*-
"""
Created on Mon Mar 24 21:05:34 2025

@author: kolja
"""

from dataclasses import dataclass
from datetime import datetime

from lockbot.lock import const
from lockbot.lock.utils import dt_or_none, convert_to_json


@dataclass
class SmartlockLog:
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