#!/usr/bin/env python3
"""
web cache and tracker
"""

import requests
import redis
from functools import wraps

# Initialize the Redis connection
store = redis.Redis()

def count_url_access(method):
    """ Decorator counting how many times a URL is accessed """
    @wraps(method)
    def wrapper(url):
        cached_key = f"cached:{url}"
        cached_data = store.get(cached_key)
        
        # If data is in cache, return it
        if cached_data:
            return cached_data.decode("utf-8")

        # If not, increment the count and fetch the data
        count_key = f"count:{url}"
        store.incr(count_key)
        html = method(url)
        
        # Store the fetched data in cache with an expiration of 10 seconds
        store.setex(cached_key, 10, html)
        return html
    return wrapper

@count_url_access
def get_page(url: str) -> str:
    """ Returns HTML content of a url """
    res = requests.get(url)
    return res.text

