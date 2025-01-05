# -*- coding: utf-8 -*-
"""
Created on Sun Jan  5 23:43:16 2025

@author: kolja
"""
import logging
import requests

from .util import handle_http_status
from .url import get_headers, url_log, url_action, url_status

logger = logging.getLogger(__name__)

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