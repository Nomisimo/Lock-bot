# -*- coding: utf-8 -*-
"""
Created on Mon Jan  6 22:03:59 2025

@author: kolja
"""
import logging
import http
import httpx
from lockbot import config


from lockbot.lock import urls
logger = logging.getLogger(__name__)


class Nuki():

    def __init__(self, api_key = None):
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
        if not code.is_success:
            logger.error(code.description)
        return code.is_success  

    def get_request(self, url):
        try: 
            with httpx.Client(headers=self.headers) as client:
                response = client.get(url)
                if not self.handle_http_status(response.status_code):
                    return None
                data = response.json()
                return data
        except Exception as e:
            logger.error(f"GET request failed for {url}\n\t{e}")
            return None
        
    def post_request(self, url):
        try:
            with httpx.Client(headers=self.headers) as client:    
                response = client.post(url)
            return self.handle_http_status(response.status_code)
        except Exception as e:
            logger.error(f"Error sending lock action: {e}")
            return False
        
    def get_smartlock(self, lock_id=None) -> list | dict:
        url = urls.url_status(lock_id=lock_id)
        data = self.get_request(url)
        return data
        
    def get_logs(self, lock_id=None, limit=5) -> list:
        url = urls.url_log(lock_id=lock_id, limit=limit)
        data = self.get_request(url)
        return data

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
        ids = [d["smartlockId"] for d in data]
        return ids
    
    def get_auth(self, lock_id=None, auth_id=None):
        url = urls.url_auth(lock_id, auth_id)
        data = self.get_request(url)
        return data
    
    def set_default_lock(self, lock_id):
        if lock_id in self.lock_ids:
            self.default_id = lock_id
            logger.info("set default lock to {self.lock_id}")
        else:
            logger.error(f"{lock_id} not in {self.lock_ids}")


class AsyncNuki(Nuki):
        
    @classmethod
    async def new(cls, api_key = None):
        self = cls(api_key=api_key)
        self.lock_ids = await self.get_smartlock_ids()
        logger.info(f"{cls.__name__} created, found locks {self.lock_ids}")
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
            logger.error(f"GET request failed for {url}\n\t{e}")
            return None
        
    async def post_request(self, url):
        try:
            async with httpx.AsyncClient(headers=self.headers) as client:    
                response = await client.post(url)
            return self.handle_http_status(response.status_code)
        except Exception as e:
            logger.error(f"Error sending lock action: {e}")
            return False
        
    async def get_smartlock(self, lock_id=None) -> list | dict:
        url = urls.url_status(lock_id=lock_id)
        data = await self.get_request(url)
        return data
        
    async def get_logs(self, lock_id=None, limit=5) -> list:
        url = urls.url_log(lock_id=lock_id, limit=limit)
        data = await self.get_request(url)
        return data
    
    async def get_auth(self, lock_id=None, auth_id=None):
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
        ids = [d["smartlockId"] for d in data]
        return ids
    