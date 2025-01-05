# -*- coding: utf-8 -*-
"""
Created on Sat Jan  4 13:21:20 2025

@author: kolja
"""

from pprint import pprint
import logging
from http import HTTPStatus
import asyncio

from urllib.parse import urljoin, urlencode

import httpx
import requests

from lockbot import config


BASE_URL = r"https://api.nuki.io/"
logger = logging.getLogger(__name__)

def handle_http_status(status):
    code = HTTPStatus(status)
    if not code.is_success:
        logger.error(code.description)
    return code.is_success  

def get_headers(api_key=None):
    if api_key is None:
        api_key = config.get("nuki", "API_KEY")
    headers = {
        "accept": "application/json",
        "Content-Type": "application/json",
        "authorization": f"Bearer {api_key}"
    }
    return headers

def url_status(lock_id=None):
    if lock_id is None:
        lock_id = config.get("nuki", "LOCK_ID")
    url = urljoin(BASE_URL, f"smartlock/{lock_id}")    
    return url

def url_log(lock_id=None, num=5):
    if lock_id is None:
        lock_id = config.get("nuki", "LOCK_ID")
    url = urljoin(BASE_URL, f"smartlock/{lock_id}/log")
    params = urlencode({"limit":num})
    return f"{url}?{params}"
    

def url_action(action="lock", lock_id=None):
    if lock_id is None:
        lock_id = config.get("nuki", "LOCK_ID")
    if action not in ("lock", "unlock"):
        raise ValueError(f"action {action} not allowed.")
    
    url = urljoin(BASE_URL, f"smartlock/{lock_id}/action/{action}")
    return url


def get_status() -> dict:
    url = url_status()
    headers = get_headers()
    
    try:
        response = requests.get(url, headers=headers)
        if not handle_http_status(response.status_code):
            return {}
        data = response.json()
        return data
    except Exception as e:
        logger.error(f"Failed to fetch state data: {e}")
        return None


def get_logs(num=5) -> list[dict]:
    url = url_log()
    headers = get_headers()
    try:
        response = requests.get(url, headers=headers)
        if not handle_http_status(response.status_code):
            return {}
        data = response.json()
        return data
    except Exception as e:
        logger.error(f"Failed to fetch logs: {e}")
        return None


def post_action(action="lock"):
    url = url_action(action=action)
    headers = get_headers()
    try:
        response = requests.post(url, headers=headers)
        return handle_http_status(response.status_code)
    except Exception as e:
        logger.error(f"Error sending lock action: {e}")
        return False


async def get_lock_status():
    LOCK_ID = config.get("nuki", "LOCK_ID")
    API_KEY = config.get("nuki", "API_KEY")
    
    
    url = f'https://api.nuki.io/smartlock/{LOCK_ID}'
    headers = {
        'accept': 'application/json',
        'authorization': f'Bearer {API_KEY}'
    }
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(url, headers=headers)
            if response.status_code != 200:
                logger.error(f"Failed to fetch battery data. Status code: {response.status_code}")
                return None
            data = response.json()
            pprint(data)
            return data
    except Exception as e:
        logger.error(f"Failed to fetch battery data: {e}")
        return None
    
async def test():
    config.load_config()
    await get_lock_status()
    
if __name__ == "__main__":
    asyncio.run(test())