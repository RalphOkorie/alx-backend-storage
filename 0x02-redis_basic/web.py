#!/usr/bin/env python3
"""
This module contains the get_page function which fetches and caches
the HTML content of a given URL. It tracks the number of accesses
to the URL and caches the result for a short duration.
"""

import requests
import redis
from typing import Callable
from functools import wraps

# Connect to Redis
r = redis.Redis()

def cache_page(expiration: int):
    """
    Decorator that caches the result of the function for a given
    expiration time and tracks the number of times the URL is accessed.

    Args:
        expiration (int): The expiration time for the cache in seconds.

    Returns:
        Callable: The wrapped function.
    """
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(url: str) -> str:
            # Track access count
            r.incr(f"count:{url}")
            # Check if URL is cached
            cached_page = r.get(url)
            if cached_page:
                return cached_page.decode('utf-8')

            # Fetch and cache the page
            page_content = func(url)
            r.setex(url, expiration, page_content)
            return page_content

        return wrapper
    return decorator

@cache_page(expiration=10)
def get_page(url: str) -> str:
    """
    Fetches the HTML content of a given URL.

    Args:
        url (str): The URL to fetch.

    Returns:
        str: The HTML content of the page.
    """
    response = requests.get(url)
    return response.text
