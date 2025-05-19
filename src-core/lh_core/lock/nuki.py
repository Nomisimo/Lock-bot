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

from lh_core.lock import (Smartlock, SmartlockLog,
                          SmartlockAuth, 
                          SmartlockAuthRequest,
                          SmartlockAuths)
logger = logging.getLogger(__name__)

from typing import override
from typing import Union, Dict, List, Any

JsonType = Union[Dict[str, Any], List[Any], str, int, float, bool, None]

class Nuki():

    def __init__(self, api_key = None):
        self.logger = logging.getLogger(__name__)
        if api_key is None:
            api_key = config.get("nuki", "api_key")
        
        self.API_KEY = api_key
        
    @classmethod
    def new(cls, api_key=None):
        self = cls(api_key=api_key)
        self.lock_ids = self.get_smartlock_ids()
        logger.info(f"{cls.__name__} created, found locks {self.lock_ids}")
        return self
    
    @property
    def headers(self):
        headers = {
            "accept": "application/json",
            "Content-Type": "application/json",
            "authorization": f"Bearer {self.API_KEY}"
        }
        return headers

    @staticmethod    
    def handle_http_status(status):
        code = http.HTTPStatus(status)
        success = (200 <= code <= 299)
        if not success:
            logger.error(f"HTTP {code} {code.description}")
        return success # code.is_success  

    # ---- request

    def get_request(self, url: str) -> JsonType:
        """ handle get requests."""
        try: 
            with httpx.Client(headers=self.headers) as client:
                response = client.get(url)
                if not self.handle_http_status(response.status_code):
                    return None
                data = response.json()
                return data
        except Exception as e:
            self.logger.error(f"GET request failed for {url}\n\t{e}")
            return None
        
    def post_request(self, url, json: JsonType = None) -> bool:
        """ handle post requests."""
        try:
            with httpx.Client(headers=self.headers) as client:    
                response = client.post(url, json=json)
            return self.handle_http_status(response.status_code)
        except Exception as e:
            self.logger.error(f"POST request failed for {url}\n\t{e}")
            return False
        
        
    def put_request(self, url: str, json: JsonType = None) -> bool:
        """ handle put requests."""
        try:
            with httpx.Client(headers=self.headers) as client:
                response = client.put(url, json=json)
                return self.handle_http_status(response.status_code)
        except Exception as e:
            self.logger.error(f"Error sending lock action: {e}")
            return False
        
    def del_request(self, url: str) -> bool:
        """ handle del requests."""
        try:
            with httpx.Client(headers=self.headers) as client:
                response = client.delete(url)
                return self.handle_http_status(response.status_code)
        except Exception as e:
            self.logger.error(f"Error sending lock action: {e}")
            return False
    
    # ---- nuki
        
    def get_smartlock(self, lock_id: str =None, raw: bool=False) -> list[Smartlock] | Smartlock | JsonType:
        """
        GET /smartlock OR /smartlock/{smartlockId}

        Parameters
        ----------
        lock_id : str, optional
            If given get only the smartlock of the id, else all smartlocks as list. The default is None.
        raw : bool, optional
            If true, the json is parsed as Smartlock. The default is False.

        Returns
        -------
        JsonType | list[Smartlock] | Smartlock
            The request result.
        """
        url = urls.url_status(lock_id=lock_id)
        data = self.get_request(url)
        if raw:
            return data
        return Smartlock.from_json(data)
        
    def get_logs(self, lock_id: str = None, limit: int =5, raw: bool=False) -> list[SmartlockLog] | JsonType:
        """
        GET /smartlock/log or /smartlock/{smartlockId}/log
 
        Parameters
        ----------
        lock_id : str, optional
            DESCRIPTION. The default is None.
        limit : int, optional
            DESCRIPTION. The default is 5.
        raw : bool, optional
            DESCRIPTION. The default is False.

        Returns
        -------
        TYPE
            DESCRIPTION.

        """
        
        url = urls.url_log(lock_id=lock_id, limit=limit)
        data = self.get_request(url)
        if raw:
            return data
        return SmartlockLog.from_json(data)
    
    def post_lock(self, lock_id: str) -> bool:
        """
        POST /smartlock/{smartlockId}/action/lock
        """
        url = urls.url_action(lock_id, action="lock")
        success = self.post_request(url)
        return success
    
    def post_unlock(self, lock_id) -> bool:
        """
        POST /smartlock/{smartlockId}/action/unlock
        """
        url = urls.url_action(lock_id, action="unlock")
        success = self.post_request(url)
        return success
    
    def get_smartlock_ids(self) -> list[int]:
        """ Extract Ids for all smartlocks."""
        data = self.get_smartlock(lock_id=None)
        ids = [d.smartlockId for d in data]
        return ids
        
    def set_default_lock(self, lock_id: str):
        """ set default smartlock."""
        if lock_id in self.lock_ids:
            self.default_id = lock_id
            self.logger.info("set default lock to {self.lock_id}")
        else:
            self.logger.error(f"{lock_id} not in {self.lock_ids}")
            
            
    # ---- nuki auth
    

    def get_auth(self, lock_id=None, auth_id=None, raw: bool=False):
        """ request smartlock auth. Either single instance or all for a given lock_id."""
        url = urls.url_auth(lock_id, auth_id)
        data = self.get_request(url)
        if raw:
            return data
        return SmartlockAuths.from_json(data)
    
    def post_auth(self, auth: dict, raw: bool=False):
        if auth is None:
            self.logger.error("post_auth: auth is None")
            return False
        if not raw:
            auth = auth.to_json()
        url = urls.url_auth(lock_id=auth["smartlockId"], auth_id=auth["id"])
        success = self.post_request(url, json=auth)
        if success:
            self.logger.info(f"Auth({auth['name']}) updated.")
        return success
    
    def put_auth(self, auth: dict, raw: bool=False):
        if auth is None:
            self.logger.error("put_auth: auth is None")
            return False
        if not raw:
            assert isinstance(auth, SmartlockAuthRequest)
            auth = auth.to_json()
        url = urls.url_auth(lock_id=None) # lock_id from auth-smartlockIds
        success = self.put_request(url, json=auth)
        if success:
            self.logger.info(f"Auth({auth['name']}) created.")
        return success
    
    def del_auth(self, auth: dict, raw: bool=False):
        if auth is None:
            self.logger.error("del_auth: auth is None")
            return False
        if not raw:
            assert isinstance(auth, SmartlockAuth)
            auth = auth.to_json()
        url = urls.url_auth(lock_id=auth["smartlockId"], auth_id=auth["id"])
        success = self.del_request(url)
        if success: 
            self.logger.info(f"Auth({auth['name']}) deleted.")
        return success
    


class AsyncNuki(Nuki):
        
    @classmethod
    async def new(cls, api_key: str = None):
        self = cls(api_key=api_key)
        self.lock_ids = await self.get_smartlock_ids()
        self.logger.info(f"{cls.__name__} created, found locks {self.lock_ids}")
        return self
    
    # ---- request
    
    async def get_request(self, url: str):
        try: 
            async with httpx.AsyncClient(headers=self.headers) as client:
                response = await client.get(url)
                if not self.handle_http_status(response.status_code):
                    return None
                data = response.json()
                return data
        except Exception as e:
            self.logger.error(f"GET request failed for {url}\n\t{e}")
            return None
        
    async def post_request(self, url: str, json=None):
        try:
            async with httpx.AsyncClient(headers=self.headers) as client:    
                response = await client.post(url)
            return self.handle_http_status(response.status_code)
        except Exception as e:
            self.logger.error(f"Error sending lock action: {e}")
            return False
        
    async def put_request(self, url: str, json=None):
         try:
             async with httpx.AsyncClient(headers=self.headers) as client:
                 response = await client.put(url, json=json)
                 return self.handle_http_status(response.status_code)
         except Exception as e:
             self.logger.error(f"Error sending lock action: {e}")
             return False
         
    async def del_request(self, url: str):
         try:
             async with httpx.AsyncClient(headers=self.headers) as client:
                 response = await client.delete(url)
                 return self.handle_http_status(response.status_code)
         except Exception as e:
             self.logger.error(f"Error sending lock action: {e}")
             return False    
        
    # ---- nuki
        
    async def get_smartlock(self, lock_id=None, raw: bool=False) -> list[Smartlock] | Smartlock:
        url = urls.url_status(lock_id=lock_id)
        data = await self.get_request(url)
        if raw:
            return data
        return Smartlock.from_json(data)
    
    async def get_logs(self, lock_id=None, limit=5, raw: bool = False) -> list[SmartlockLog]:
        url = urls.url_log(lock_id=lock_id, limit=limit)
        data = await self.get_request(url)
        if raw:
            return data
        return SmartlockLog.from_json(data)
    
    async def post_lock(self, lock_id) -> bool:
        url = urls.url_action(lock_id, action="lock")
        success = await self.post_request(url)
        return success
    
    async def post_unlock(self, lock_id) -> bool:
        url = urls.url_action(lock_id, action="unlock")
        success = await self.post_request(url)
        return success
    
    async def get_smartlock_ids(self) -> list[int]:
        data = await self.get_smartlock(lock_id=None)
        ids = [d.smartlockId for d in data]
        return ids
    
    # ---- nuki auth
    
    async def get_auth(self, lock_id=None, auth_id=None, raw: bool=False):
        url = urls.url_auth(lock_id, auth_id)
        data = await self.get_request(url)
        if raw:
            return data
        return SmartlockAuths.from_json(data)
    
    async def post_auth(self, auth: dict, raw: bool=False):
        if auth is None:
            self.logger.error("post_auth: auth is None")
            return False
        if not raw:
            auth = auth.to_json()
        url = urls.url_auth(lock_id=auth["smartlockId"], auth_id=auth["id"])
        success = await self.post_request(url, json=auth)
        if success:
            self.logger.info(f"Auth({auth['name']}) updated.")
        return success
    
    async def put_auth(self, auth: dict, raw: bool=False):
        if auth is None:
            self.logger.error("put_auth: auth is None")
            return False
        if not raw:
            assert isinstance(auth, SmartlockAuthRequest)
            auth = auth.to_json()
        url = urls.url_auth(lock_id=None) # lock_id from auth-smartlockIds
        success = await self.put_request(url, json=auth)
        if success:
            self.logger.info(f"Auth({auth['name']}) created.")
        return success
    
    async def del_auth(self, auth: dict, raw: bool=False):
        if auth is None:
            self.logger.error("del_auth: auth is None")
            return False
        if not raw:
            assert isinstance(auth, SmartlockAuth)
            auth = auth.to_json()
        url = urls.url_auth(lock_id=auth["smartlockId"], auth_id=auth["id"])
        success = await self.del_request(url)
        if success: 
            self.logger.info(f"Auth({auth['name']}) deleted.")
        return success

    
    
    
class DevAsyncNuki(AsyncNuki):
    
    @override
    async def post_lock(self, lock_id) -> bool:
        self.logger.warning("locking disabled in dev mode")
        return False
    
    @override
    async def post_unlock(self, lock_id) -> bool:
        self.logger.warning("unlocking disabled in dev mode")
        return False