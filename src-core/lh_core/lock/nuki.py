# -*- coding: utf-8 -*-
"""
Classes to handle requests to the NUKI API

@author: kolja
"""
import logging
import http
import httpx
from lh_core import config

from lh_core.lock import urls

from lh_core.lock import (Smartlock, SmartlockLog, SmartlockAuth)
# from lh_core.lock import (SmartlockAuth, SmartlockAuthCreate, SmartlockAuthUpdate, SmartlockAuths)
                          

from typing import override
from typing import Union, Dict, List, Any, Optional

JsonType = Union[Dict[str, Any], List[Any], str, int, float, bool, None]


class Nuki():
    def __init__(self, api_key = None):
        self.logger = logging.getLogger(__name__)
        if api_key is None:
            api_key = config.get("nuki", "api_key")
        self.API_KEY = api_key
        self.lock_ids = []
        self.default_id = None
        
    @property
    def headers(self):
        return {
            "accept": "application/json",
            "Content-Type": "application/json",
            "authorization": f"Bearer {self.API_KEY}"
        }

    def _request(self, method: str, url: str, json=None) -> Optional[Union[dict, bool]]:
        try:
            with httpx.Client(headers=self.headers) as client:
                response = client.request(method, url, json=json)
                code = http.HTTPStatus(response.status_code)
                if not (200 <= code <= 299):
                    self.logger.error(f"HTTP {code} - {code.description}\n\t{method} - {url}")
                    return None if method == "GET" else False
                return response.json() if method == "GET" else True
        except Exception as e:
            self.logger.error(f"{method} request failed for {url}\n\t{e}")
            return None if method == "GET" else False

    # def _handle_http_status(self, status: int) -> bool:
    #     code = http.HTTPStatus(status)
    #     if not (200 <= status <= 299):
    #         self.logger.error(f"HTTP {code} - {code.description}")
    #         return False
    #     return True
    
    # ---- shortcut functions 
    
    def get_smartlock(self, lock_id: str =None, raw: bool=False) -> list[Smartlock] | Smartlock | JsonType:
        """
        GET /smartlock OR /smartlock/{smartlockId}
        """
        url = urls.url_status(lock_id=lock_id)
        data = self._request("GET", url)
        return data if raw else Smartlock.from_json(data)

    def retrieve_smartlock_ids(self) -> list[int]:
        """ Extract Ids for all smartlocks."""
        data = self.get_smartlock(lock_id=None)
        self.lock_ids = [d.smartlockId for d in data]
        return self.lock_ids

    def get_logs(self, lock_id: str = None, limit: int = 5, raw: bool = False):
        """
        GET /smartlock/log or /smartlock/{smartlockId}/log
        """
        url = urls.url_log(lock_id, limit=limit)
        data = self._request("GET", url)
        return data if raw else SmartlockLog.from_json(data)
    
    def post_lock(self, lock_id: str) -> bool:
        """
        POST /smartlock/{smartlockId}/action/lock
        """
        url = urls.url_action(lock_id, action="lock")
        return self._request("POST", url)
    
    def post_unlock(self, lock_id) -> bool:
        """
        POST /smartlock/{smartlockId}/action/unlock
        """
        url = urls.url_action(lock_id, action="unlock")
        return self._request("POST", url)
    
    def set_default_lock(self, lock_id: str = None):
        """ set default smartlock."""
        if lock_id is None:
            lock_id = int(config.get("nuki", "lock_id"))
        if lock_id in self.lock_ids:
            self.default_id = lock_id
            self.logger.info(f"set default lock to {self.default_id}")
        else:
            self.logger.error(f"{lock_id} not in {self.lock_ids}")
            
    def get_auths(self, lock_id: str = None, raw: bool = False):
        """
        GET /smartlock/auth or /smartlock/{smartlockId}/auth
        """
        url = urls.url_auth(lock_id)
        data = self._request("GET", url)
        return data if raw else SmartlockAuth.from_json(data)
            

class AsyncNuki(Nuki):

    @override
    async def _request(self, method: str, url: str, json=None) -> Optional[Union[dict, bool]]:
        try:
            async with httpx.AsyncClient(headers=self.headers) as client:
                response = await client.request(method, url, json=json)
                code = http.HTTPStatus(response.status_code)
                if not (200 <= code <= 299):
                    self.logger.error(f"HTTP {code} - {code.description}\n\t{method} - {url}")
                    return None if method == "GET" else False
                return response.json() if method == "GET" else True
        except Exception as e:
            self.logger.error(f"{method} request failed for {url}\n\t{e}")
            return None if method == "GET" else False

    # ---- shortcut functions 
    @override
    async def get_smartlock(self, lock_id: str =None, raw: bool=False) -> list[Smartlock] | Smartlock | JsonType:
        """
        GET /smartlock OR /smartlock/{smartlockId}
        """
        url = urls.url_status(lock_id=lock_id)
        data = await self._request("GET", url)
        return data if raw else Smartlock.from_json(data)

    @override
    async def get_logs(self, lock_id: str = None, limit: int = 5, raw: bool = False):
        """
        GET /smartlock/log or /smartlock/{smartlockId}/log
        """
        url = urls.url_log(lock_id, limit=limit)
        data = await self._request("GET", url)
        return data if raw else SmartlockLog.from_json(data)
    
    @override
    async def post_lock(self, lock_id: str) -> bool:
        """
        POST /smartlock/{smartlockId}/action/lock
        """
        url = urls.url_action(lock_id, action="lock")
        return await self._request("POST", url)
    
    @override
    async def post_unlock(self, lock_id) -> bool:
        """
        POST /smartlock/{smartlockId}/action/unlock
        """
        url = urls.url_action(lock_id, action="unlock")
        return await self._request("POST", url)
    
    
    @override
    async def retrieve_smartlock_ids(self) -> list[int]:
        """ Extract Ids for all smartlocks."""
        data = await self.get_smartlock(lock_id=None)
        self.lock_ids = [d.smartlockId for d in data]
        return self.lock_ids
    
    
    @override
    async def get_auths(self, lock_id: str = None, raw: bool = False):
        """
        GET /smartlock/auth or /smartlock/{smartlockId}/auth
        """
        url = urls.url_auth(lock_id)
        data = await self._request("GET", url)
        return data if raw else SmartlockAuth.from_json(data)
            
    
class DevAsyncNuki(AsyncNuki):
    
    @override
    async def post_lock(self, lock_id) -> bool:
        self.logger.warning("locking disabled in dev mode")
        return False
    
    @override
    async def post_unlock(self, lock_id) -> bool:
        self.logger.warning("unlocking disabled in dev mode")
        return False