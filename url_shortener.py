import hashlib
import time
from typing import Optional


class URLShortener:
    """URL shortener with shared in-memory storage."""
    
    _url_map: dict = {}
    _short_code_map: dict = {}
    _counter: int = 0
    
    @classmethod
    def reset(cls):
        """Reset all storage for testing."""
        cls._url_map.clear()
        cls._short_code_map.clear()
        cls._counter = 0
    
    @classmethod
    def shorten(cls, url: str) -> str:
        """Shorten a URL and return the short code."""
        # Generate a short code using hash of URL + timestamp for uniqueness
        timestamp = int(time.time() * 1000000)
        combined = f"{url}{timestamp}"
        short_code = hashlib.md5(combined.encode()).hexdigest()[:8]
        
        # Ensure uniqueness
        while short_code in cls._short_code_map:
            cls._counter += 1
            short_code = hashlib.md5(f"{combined}{cls._counter}".encode()).hexdigest()[:8]
        
        cls._short_code_map[short_code] = url
        cls._url_map[url] = short_code
        
        return short_code
    
    @classmethod
    def expand(cls, short_code: str) -> Optional[str]:
        """Expand a short code back to the original URL."""
        return cls._short_code_map.get(short_code)


def shorten_url(url: str) -> str:
    """Convenience function to shorten a URL."""
    return URLShortener.shorten(url)


def expand_url(short_code: str) -> Optional[str]:
    """Convenience function to expand a short code."""
    return URLShortener.expand(short_code)
