# -*- coding: utf-8 -*-
"""
Created on Sun Jan  5 23:42:54 2025

@author: kolja
"""
import logging
from urllib.parse import urljoin, urlencode

from lockbot import config

BASE_URL = r"https://api.nuki.io/"

logger = logging.getLogger(__name__)


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