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

from lh_core.lock.const import AUTH_TYPE
from lh_core.lock.utils import dt_or_none, convert_to_json, tz_as_local, nuki_datetime_encoder
from lh_core.lock.utils import generate_code, total_minutes

from pydantic import BaseModel, Field
from typing import Optional, TypeVar, Union, List, Type
T = TypeVar("T", bound="BaseModel")

class SmartlockAuth(BaseModel):
    id: str =           Field(..., description="Eindeutige ID der Authentifizierung")
    smartlockId: int =  Field(..., description="ID des zugehörigen Smartlocks")
    accountUserId: Optional[int] = Field(None, description="ID des verknüpften Account-Benutzers")
    authId: Optional[int] = Field(None, description="ID der verknüpften Smartlock-Authorisation")
    
    name: str =         Field(..., description="Name des Benutzers oder Codes")
    type: AUTH_TYPE =   Field(..., description="Typ der Berechtigung (z. B. 2 = App, 13 = Keypad-Code)")
    code: Optional[int] = Field(None, description="Keypad-Code, falls Typ 13")
    enabled: bool =     Field(..., description="Ob die Berechtigung aktiv ist")
    remoteAllowed: Optional[bool] = Field(None, description="Ob Fernzugriff erlaubt ist")
    
    allowedFromDate:  Optional[datetime] = Field(None, description="Zugriff ab diesem Datum erlaubt")
    allowedUntilDate: Optional[datetime] = Field(None, description="Zugriff nur bis zu diesem Datum")
    allowedWeekDays:  Optional[int] = Field(None, description="Bitmaske der erlaubten Wochentage")
    allowedFromTime:  Optional[int] = Field(None, description="Zugriffszeitfenster ab (Minuten seit Mitternacht)")
    allowedUntilTime: Optional[int] = Field(None, description="Zugriffszeitfenster bis (Minuten seit Mitternacht)")
    
    lockCount:      Optional[int] = Field(None, description="Anzahl der Nutzungen")
    lastActiveDate: Optional[datetime] = Field(None, description="Letzter Zeitpunkt der Nutzung")
    creationDate:   Optional[datetime] = Field(None, description="Zeitpunkt der Erstellung")
    updateDate:     Optional[datetime] = Field(None, description="Zeitpunkt der letzten Änderung")
    
    operationId:    Optional[dict] = None
    error:          Optional[str] = None
    appId:          Optional[int] = None
    authTypeAsString: Optional[str] = None



    def to_json(self):
        return self.model_dump(mode="json", exclude_none=True)
    
    class Config:
        json_encoders = {datetime: nuki_datetime_encoder}
    
    @classmethod
    def from_json(cls: Type[T], data: Union[dict, List[dict]]) -> Union[T, List[T]]:
        if isinstance(data, list):
            return [cls(**item) for item in data]
        return cls(**data)
    
    
class SmartlockAuthUpdate(BaseModel):
    name: str = Field(..., description="Name der Berechtigung")
    code: Optional[str] = Field(None, description="Zugangscode für Keypad")
    
    allowedFromDate:  Optional[datetime] = Field(None, description="Zugriff erlaubt ab Datum")
    allowedUntilDate: Optional[datetime] = Field(None, description="Zugriff erlaubt bis Datum")
    allowedWeekDays:  Optional[int] = Field(None, description="Bitmaske für erlaubte Wochentage")
    allowedFromTime:  Optional[int] = Field(None, description="Zugriffszeitfenster ab (Minuten seit Mitternacht)")
    allowedUntilTime: Optional[int] = Field(None, description="Zugriffszeitfenster bis (Minuten seit Mitternacht)")
    
    accountUserId:    Optional[int]  = Field(None, description="ID des zugewiesenen Accounts")
    enabled:          Optional[bool] = Field(None, description="Ist die Berechtigung aktiviert?")
    remoteAllowed:    Optional[bool] = Field(None, description="Ist Fernzugriff erlaubt?")
    
    def to_json(self):
        return self.model_dump(mode="json", exclude_none=True)
    

class SmartlockAuthCreate(BaseModel):
    name: str = Field(..., description="Name der Berechtigung")
    remoteAllowed:    bool = Field(..., description="Ist Fernzugriff erlaubt?")
    code: Optional[str] = Field(None, description="Zugangscode für Keypad")
    type: Optional[AUTH_TYPE] = Field(None, description="Art des Zugangs.")
    allowedFromDate:  Optional[datetime] = Field(None, description="Zugriff erlaubt ab Datum")
    allowedUntilDate: Optional[datetime] = Field(None, description="Zugriff erlaubt bis Datum")
    allowedWeekDays:  Optional[int] = Field(None, description="Bitmaske für erlaubte Wochentage")
    allowedFromTime:  Optional[int] = Field(None, description="Zugriffszeitfenster ab (Minuten seit Mitternacht)")
    allowedUntilTime: Optional[int] = Field(None, description="Zugriffszeitfenster bis (Minuten seit Mitternacht)")
    
    accountUserId:    Optional[int]  = None
    smartActionsEnabled: Optional[bool] = None
    
    def to_json(self):
        return self.model_dump(mode="json", exclude_none=True)
    

# name*	[...]
# allowedFromDate	[...]
# allowedUntilDate	[...]
# allowedWeekDays	[...]
# allowedFromTime	integer($int32)
# The allowed from time (in minutes from midnight)

# allowedUntilTime	[...]
# accountUserId	[...]
# remoteAllowed*	[...]
# smartActionsEnabled	[...]
# type	integer($int32)
# The optional type of the auth 0 .. app (default), 2 .. fob, 13 .. keypad

# code
    
    
    
@dataclass    
class SmartlockAuthRequest:
    name: str
    remoteAllowed: bool
    
    allowedFromDate	: datetime = None
    allowedUntilDate: datetime = None
    allowedWeekDays:    int = None
    allowedFromTime	:    int = None
    allowedUntilTime:   int = None
    
    code: str = None
    accountUserId: int = None
    smartlockIds: list[int] = None
    smartActionsEnabled : bool = None
    type: AUTH_TYPE = None
    
    def __post_init__(self):
        self.type = AUTH_TYPE(self.type)        
        self.allowedFromDate = dt_or_none(self.allowedFromDate)
        self.allowedUntilDate = dt_or_none(self.allowedUntilDate)
        
        self.logger = logging.getLogger(__name__)
    
        
    def to_json(self):
        res = convert_to_json(self)
        return res
    




class SmartlockAuths:
    auths: list[SmartlockAuth]
    
    _selected: SmartlockAuth
    _updated: SmartlockAuth
    
    def __init__(self, auths: list[SmartlockAuth]):
        
        self.auths = [SmartlockAuth(**a) for a in auths]
        self._selected: SmartlockAuth = None
        self._updated: SmartlockAuth = None
        
        self.logger = logging.getLogger(__name__)
    
    # def __post_init__(self):
    #     self.auths = [SmartlockAuth(**a) for a in self.auths]
    
    def _get_names(self) -> set[str]:
        return {auth.name for auth in self.auths if auth.name is not None}
    
    def _get_codes(self) -> set[int]:
        return {auth.code for auth in self.auths if auth.code is not None}
    
    # ---- parser
        
    def to_json(self):
        res = [convert_to_json(a) for a in self.auths]
        return res
    
    @classmethod
    def from_json(cls, data):
        if isinstance(data, list):        
            return cls(data)
        return SmartlockAuth(**data)

    # ---- selection
        
    def selected(self) -> SmartlockAuth | None:
        """ Return selection (without updates)."""
        return self._selected
    
    def updated(self) -> SmartlockAuth | None:
        """ Return current object with updates."""
        if self._selected is None:
            self.logger.info("No auth selected")
        elif self._selected == self._updated:
            self.logger.info("Selected auth has not changed.")
            return None
        elif isinstance(self._updated, SmartlockAuthRequest):
            self.logger.warning("Selected auth is not created yet.")
        return self._updated
    
    def created(self) -> SmartlockAuthRequest | None:
        """ Return created object."""
        if not isinstance(self._updated, SmartlockAuthRequest):
            self.logger.info("No auth created.")
            return None
        return self._updated
    
    
    def reset_selection(self) -> Self:
        """ Reset selection."""
        self._selected = None
        self._updated = None
        return self
    
    
    def by_name(self, name) -> Self:
        """ select auth by name."""
        for auth in self.auths:
            if auth.name == name:
                self.reset_selection()
                self._selected = auth
                self._updated = replace(auth)
                return self
        self.logger.warning(f"{name=} not found.")
        self.reset_selection()
        return self
    
    # TODO: select by code
           
    def create(self, name: str, lock_ids: list[int]) -> Self:
        """ Create and select new auth object."""
        if name in self._get_names():
            self.logger.warning(f"{name=} already used")
            return self
        
        self.reset_selection()
        if isinstance(lock_ids, int):
            lock_ids=[lock_ids]
        new = SmartlockAuthRequest(
            name=name, 
            type=AUTH_TYPE.keypad_code,
            code=None,
            smartlockIds=lock_ids, 
            remoteAllowed=True,
            )
        self._updated = new
        self.rotate_code()        
        return self
        
        
    def delete(self, name: str):
        """ return selection by name."""
        self.by_name(name)
        return self.selected()
    
    # ---- update
    
    
    def set_name(self, name: str) -> Self:
        """ Change name of selection."""
        if name in self._get_names():
            self.logger.warning("name is already used")
        elif self._updated:
            self._updated.name = name
        return self
        
    def set_code(self, code: int) -> Self:
        """ Change code of selection."""
        if code in self._get_codes():
            self.logger.warning("code is not valid")
        elif self._updated:
            self._updated.code = code
        return self
    
    def rotate_code(self, created: bool=False) -> Self:
        """ Change code of selection to new random code. 
        """
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
        """ Update Enabled for selection. If selection not given: toggle current value."""
        if self._updated is None:
            pass
        elif enable is None:
            self._updated.enabled = not self._updated.enabled
        else: 
            self._updated.enabled = enable
        return self
    
    def set_period(self, from_date: datetime, until_date: datetime) -> Self:
        if self._updated is None:
            return self
                
        self._updated.allowedWeekDays = 127
        self._updated.allowedFromTime = 0
        self._updated.allowedUntilTime = 0
        self._updated.allowedFromDate = tz_as_local(from_date)
        self._updated.allowedUntilDate = tz_as_local(until_date)
        return self
    
    def clear_period(self) -> Self:
        if self._updated is None:
            return self
        
        self._updated.allowedWeekDays = 0
        self._updated.allowedFromTime = None
        self._updated.allowedUntilTime = None
        self._updated.allowedFromDate = None
        self._updated.allowedUntilDate = None
        return self
    
        
    
    # TODO: Weekdays
    # TODO: AllowedTime
        

     
    