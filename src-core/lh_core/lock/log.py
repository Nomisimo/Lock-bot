# -*- coding: utf-8 -*-
"""
Created on Mon Mar 24 21:05:34 2025

@author: kolja
"""

from datetime import datetime
from typing import Optional, Dict, Any

from lh_core.lock import const
from lh_core.lock.utils import NukiModel

class SmartlockLog(NukiModel):
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
    
    
    
