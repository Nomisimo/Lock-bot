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
    if lock_id:
        url = urljoin(BASE_URL, f"smartlock/{lock_id}")    
    else:
        url = urljoin(BASE_URL, "smartlock")    
    return url

def url_log(lock_id=None, limit=5):
    if lock_id:
        url = urljoin(BASE_URL, f"smartlock/{lock_id}/log")
    else:
        url = urljoin(BASE_URL, "smartlock/log")
    params = urlencode({"limit":limit})
    return f"{url}?{params}"
    

def url_action(lock_id, action="lock"):
    if action not in ("lock", "unlock"):
        raise ValueError(f"action {action} not allowed.")
    
    url = urljoin(BASE_URL, f"smartlock/{lock_id}/action/{action}")
    return url


def url_auth(lock_id=None, auth_id=None):
    if lock_id is None:
        url = urljoin(BASE_URL, "smartlock/auth")
    elif auth_id is None:
        url = urljoin(BASE_URL, f"smartlock/{lock_id}/auth")
    else:
        url = urljoin(BASE_URL, f"smartlock/{lock_id}/auth/{id}")
    return url