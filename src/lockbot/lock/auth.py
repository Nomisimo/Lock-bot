# -*- coding: utf-8 -*-
"""
Created on Sun Mar 23 22:20:29 2025

Handeling (name, code) authentifications.

@author: kolja
"""

from dataclasses import dataclass, replace
from datetime import datetime
from typing import  Self
import logging

from lockbot.lock import const
from lockbot.lock.model import dt_or_none, convert_to_json

import random

def generate_code(): 
    return int("".join(str(i) for i in random.choices(range(1,10), k=6)))

def total_minutes(dt: datetime | pytime) -> int:
    return dt.minute + dt.hour*60


@dataclass
class SmartlockAuth:
    smartlockId:    str 
    type:           int # ToDo: create const.AUTH_TYPE
    name:           str
    id:             str = None
    enabled:        bool = False
    remoteAllowed:  bool = False
    lockCount:      int = None
    
    accountUserId:  int = None
    authId:         int = None
    code:           int = None
    fingerprints:   dict = None
    
    allowedFromDate	: datetime = None
    allowedUntilDate: datetime = None
    allowedWeekDays:    int = None
    allowedFromTime	:    int = None
    allowedUntilTime:   int = None
    lastActiveDate: datetime = None
    creationDate:   datetime = None
    updateDate:     datetime = None
    operationId:    dict = None
    error:          str = None
    appId:          str = None
    authTypeAsString: str = None
    
    
    def __post_init__(self):
        self.type = const.AUTH_TYPE(self.type)
        
        self.allowedFromDate = dt_or_none(self.allowedFromDate)
        self.allowedUntilDate = dt_or_none(self.allowedUntilDate)
        self.creationDate = dt_or_none(self.creationDate)
        
        self.updateDate = dt_or_none(self.updateDate) 
        self.lastActiveDate = dt_or_none(self.lastActiveDate)
    
    def to_json(self):
        res = convert_to_json(self)
        return res
    
    @classmethod
    def from_json(cls, data):
        if isinstance(data, list):        
            return SmartlockAuths(data)
        return cls(**data)
    
        
    def __repr__(self):
        return (f"{self.__class__.__name__}({self.authId},\t"
                f"name='{self.name}',\t"
                f"code={self.code})"
                )
    

@dataclass
class SmartlockAuths:
    auths: list[SmartlockAuth]
    
    def __post_init__(self):
        self.auths = [SmartlockAuth(**a) for a in self.auths]
        
        self._selected = None
        self._updated = None
        
    def to_json(self):
        res = [convert_to_json(a) for a in self.auths]
        return res
    
    @classmethod
    def from_json(cls, data):
        if isinstance(data, list):        
            return cls(data)
        return SmartlockAuth(**data)
            
    def _get_names(self):
        return {auth.name for auth in self.auths if auth.name is not None}
    
    def _get_codes(self):
        return {auth.code for auth in self.auths if auth.code is not None}
    
    def by_name(self, name) -> Self:
        """ select auth by name."""
        for auth in self.auths:
            if auth.name == name:
                self._selected = auth
                self._updated = replace(auth)
                return self
        logging.info(f"{name=} not found.")
        self._selected = None
        self._updated = None
        return self
        
    def set_name(self, name) -> Self:
        """ update name """
        if name in self._get_names():
            logging.info("name is already used")
        elif self._updated:
            self._updated.name = name
        return self
        
    def set_code(self, code) -> Self:
        """ update code."""
        if code in self._get_codes():
            logging.info("code is already used")
        elif self._updated:
            self._updated.code = code
        return self
    
    def rotate_code(self) -> Self:
        """ generate random code."""
        if self._updated is None:
            return self
        used_codes = self._get_codes()
        for i in range(3):
            code = generate_code()
            if code not in used_codes:
                self._updated.code = code
                return self
        raise ValueError(f"no new code generated after {i} tries.")
            
    def update_enable(self, enable: bool=None) -> Self:
        """ toggle enabled."""
        if self._updated is None:
            pass
        elif enable is None:
            self._updated.enabled = not self._updated.enabled
        else: 
            self._updated.enabled = enable
        return self
    
    def set_dt(self, from_date, until_date) -> Self:
        raise NotImplementedError()
        
    def create(self, *args, **kwargs):
        raise NotImplementedError()
        
    def delete(self, name: str):
        raise NotImplementedError()
        
    def selected(self):
        """ return selected auth."""
        return self._selected
    
    def updated(self):
        """ return updated auth. Return None if nothing selected or nothing has changed."""
        if self._selected is None:
            logging.info("nothing selected")
        elif self._selected == self._updated:
            logging.info("nothing changed")
            return None
        return self._updated
        
    
    
### OLD CODE
# ### ZEITBEGRENZUNG: braucht den ganzen Block
# def auth_set_dt(name: str, from_date: datetime = None, until_date: datetime = None):
#     AUTHS = nuki.get_auth(lock_id, raw=True)
#     a = auth_by_name(AUTHS, name)
#     if not a:
#         logging.warning(f"{name=} not found")
#         return False
#     print(a)
#     if from_date is None:
#         a["allowedWeekDays"] = 0
#         a["allowedFromTime"] = None
#         a["allowedUntilTime"] = None
#         a["allowedFromDate"] = None
#         a["allowedUntilDate"] = None
#     else:
         
#         a["allowedWeekDays"] = 127
#         a["allowedFromTime"] = 0
#         a["allowedUntilTime"] = 0
#         a["allowedFromDate"] = dt_to_str(from_date)
#         a["allowedUntilDate"] = dt_to_str(until_date)
        
#     val = nuki.update_auth(lock_id, auth_id=a["id"], data=a, raw=True)
#     logging.info(f"{name=} set date={from_date, until_date}")
#     # return val

# auth_enable("TESTING", True)
# d1 = datetime(2025, 4, 21, 8)
# d2 = datetime(2025, 4, 21, 18)
# d1, d2 = None, None
# auth_set_dt("TESTING", d1, d2)

    