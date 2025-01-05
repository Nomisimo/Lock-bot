# -*- coding: utf-8 -*-
"""
Created on Sat Jan  4 13:31:35 2025

@author: kolja
"""

import requests
from pprint import pprint
from lockbot import config
import logging
from http import HTTPStatus


from urllib.parse import urljoin, urlencode

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


BASE_URL = r"https://api.nuki.io/"


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

def handle_status(status):
    code = HTTPStatus(status)
    if not code.is_success:
        logger.error(code.description, "lock")
    return code.is_success    

def get_status() -> dict:
    url = url_status()
    headers = get_headers()
    
    try:
        response = requests.get(url, headers=headers)
        if not handle_status(response.status_code):
            return {}
        data = response.json()
        return data
    except Exception as e:
        logger.error(f"Failed to fetch state data: {e}",)
        return None

def get_logs(num=5) -> list[dict]:
    url = url_log()
    headers = get_headers()
    try:
        response = requests.get(url, headers=headers)
        if not handle_status(response.status_code):
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
        return handle_status(response.status_code)
    except Exception as e:
        logger.error(f"Error sending lock action: {e}")
        return False
        

if __name__ == "__main__":
    config.load_config()
    # state = (get_status()["state"])
    # get_logs()
    
    post_action(action="lock")




