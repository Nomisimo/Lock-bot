# -*- coding: utf-8 -*-
"""
Created on Mon Mar 24 21:05:34 2025

@author: kolja
"""

from dataclasses import dataclass
from datetime import datetime, timezone

from lh_core.lock import const
from lh_core.lock.utils import dt_or_none, nuki_datetime_encoder

from typing import Optional, TypeVar, Union, List, Type

from typing import Optional, Dict, Any
from pydantic import BaseModel

T = TypeVar("T", bound="BaseModel")

class SmartlockLog(BaseModel):
    id: str
    smartlockId: int
    deviceType: const.DEVICE_TYPE  
    name: str
    action: const.ACTION            
    trigger: const.TRIGGER          
    state: const.LOG_STATE          
    autoUnlock: bool
    date: datetime

    accountUserId: Optional[int] = None
    authId: Optional[str] = None
    openerLog: Optional[Dict[str, Any]] = None  # TODO: refine substructure if needed
    ajarTimeout: Optional[int] = None
    source: Optional[const.LOG_SOURCE] = None
    error: Optional[str] = None
    
    def to_json(self):
        return self.model_dump(mode="json", exclude_none=True)
    
    class Config:
        json_encoders = {datetime: nuki_datetime_encoder}

    @classmethod
    def from_json(cls: Type[T], data: Union[dict, List[dict]]) -> Union[T, List[T]]:
        if isinstance(data, list):
            return [cls(**item) for item in data]
        return cls(**data)