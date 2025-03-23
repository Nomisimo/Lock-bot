# -*- coding: utf-8 -*-
"""
Classes to handle requests to the NUKI API

@author: kolja
"""
import logging
import http
import httpx
from lockbot import config

from lockbot.lock import urls
from lockbot.lock import model
logger = logging.getLogger(__name__)

from typing import override


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

    def get_request(self, url):
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
        
    def post_request(self, url, json=None):
        try:
            with httpx.Client(headers=self.headers) as client:    
                response = client.post(url, json=json)
                self.logger.debug(response)
            return self.handle_http_status(response.status_code)
        except Exception as e:
            self.logger.error(f"POST request failed for {url}\n\t{e}")
            return False
        
        
    def put_request(self, url, json=None):
        try:
            with httpx.Client(headers=self.headers) as client:
                response = client.put(url, json=json)
                return self.handle_http_status(response.status_code)
        except Exception as e:
            self.logger.error(f"Error sending lock action: {e}")
            return False
        
    def del_request(self, url):
        try:
            with httpx.Client(headers=self.headers) as client:
                response = client.delete(url)
                return self.handle_http_status(response.status_code)
        except Exception as e:
            self.logger.error(f"Error sending lock action: {e}")
            return False
        
    def get_smartlock(self, lock_id=None, raw: bool=False) -> list[model.Smartlock] | model.Smartlock:
        url = urls.url_status(lock_id=lock_id)
        data = self.get_request(url)
        if raw:
            return data
        if isinstance(data, list):
            return [model.Smartlock(**d) for d in data]
        return model.Smartlock(**data)
        
    def get_logs(self, lock_id=None, limit=5, raw: bool=False) -> list[model.LogEntry]:
        url = urls.url_log(lock_id=lock_id, limit=limit)
        data = self.get_request(url)
        if raw:
            return data
        return [model.LogEntry(**d) for d in data]

    def get_auth(self, lock_id=None, auth_id=None, raw: bool=False):
        url = urls.url_auth(lock_id, auth_id)
        data = self.get_request(url)
        if raw:
            return data
        return [model.SmartlockAuth(**a) for a in data]
    
    def update_auth(self, lock_id, auth_id, data, raw: bool=True):
        url = urls.url_auth(lock_id, auth_id)
        if not raw:
            raise ValueError("not supported")
        success = self.post_request(url, json=data)
        return success
    
    def post_lock(self, lock_id) -> bool:
        url = urls.url_action(lock_id, action="lock")
        success = self.post_request(url)
        return success
    
    def post_unlock(self, lock_id) -> bool:
        url = urls.url_action(lock_id, action="unlock")
        success = self.post_request(url)
        return success
    
    def get_smartlock_ids(self) -> list[int]:
        data = self.get_smartlock(lock_id=None)
        ids = [d.smartlockId for d in data]
        return ids
        
    def set_default_lock(self, lock_id):
        if lock_id in self.lock_ids:
            self.default_id = lock_id
            self.logger.info("set default lock to {self.lock_id}")
        else:
            self.logger.error(f"{lock_id} not in {self.lock_ids}")


class AsyncNuki(Nuki):
        
    @classmethod
    async def new(cls, api_key = None):
        self = cls(api_key=api_key)
        self.lock_ids = await self.get_smartlock_ids()
        self.logger.info(f"{cls.__name__} created, found locks {self.lock_ids}")
        return self
    
    async def get_request(self, url):
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
        
    async def post_request(self, url):
        try:
            async with httpx.AsyncClient(headers=self.headers) as client:    
                response = await client.post(url)
            return self.handle_http_status(response.status_code)
        except Exception as e:
            self.logger.error(f"Error sending lock action: {e}")
            return False
        
    async def get_smartlock(self, lock_id=None, raw: bool=False) -> list[model.Smartlock] | model.Smartlock:
        url = urls.url_status(lock_id=lock_id)
        data = await self.get_request(url)
        if raw:
            return data
        if isinstance(data, list):
            return [model.Smartlock(**d) for d in data]
        return model.Smartlock(**data)     
    
    async def get_logs(self, lock_id=None, limit=5, raw: bool = False) -> list[model.LogEntry]:
        url = urls.url_log(lock_id=lock_id, limit=limit)
        data = await self.get_request(url)
        if raw:
            return data
        return [model.LogEntry(**d) for d in data]
    
    async def get_auth(self, lock_id=None, auth_id=None, raw: bool=False):
        url = urls.url_auth(lock_id, auth_id)
        data = await self.get_request(url)
        return data

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
    
    
    
class DevAsyncNuki(AsyncNuki):
    
    @override
    async def post_lock(self, lock_id) -> bool:
        self.logger.warning("locking disabled in dev mode")
        return False
    
    @override
    async def post_unlock(self, lock_id) -> bool:
        self.logger.warning("unlocking disabled in dev mode")
        return False