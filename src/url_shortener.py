import hashlib
from typing import Optional


class URLShortener:
    """Minimal URL shortener with in-memory storage."""

    def __init__(self):
        self._url_map: dict[str, str] = {}
        self._short_map: dict[str, str] = {}

    def _generate_short_code(self) -> str:
        """Generate a unique short code."""
        while True:
            code = hashlib.sha256(str(self._url_map).encode()).hexdigest()[:8]
            if code not in self._short_map:
                return code

    def shorten(self, url: str) -> Optional[str]:
        """Shorten a URL and return the short code.
        
        Args:
            url: The full URL to shorten
            
        Returns:
            The short code, or None if the URL is invalid
            
        Raises:
            ValueError: If the URL is invalid
        """
        if not self._is_valid_url(url):
            return None
        
        short_code = self._generate_short_code()
        self._url_map[short_code] = url
        self._short_map[url] = short_code
        return short_code

    def expand(self, short_code: str) -> Optional[str]:
        """Expand a short code back to the original URL.
        
        Args:
            short_code: The short code to expand
            
        Returns:
            The original URL, or None if not found
        """
        return self._url_map.get(short_code)

    def _is_valid_url(self, url: str) -> bool:
        """Check if a string is a valid URL."""
        if not url or not isinstance(url, str):
            return False
        
        # Basic URL validation
        if not (url.startswith('http://') or url.startswith('https://')):
            return False
        
        # Check for basic structure
        if '://' not in url:
            return False
        
        return True


# Singleton instance for convenience functions
_shortener: Optional[URLShortener] = None


def shorten_url(url: str) -> Optional[str]:
    """Convenience function to shorten a URL.
    
    Args:
        url: The full URL to shorten
        
    Returns:
        The short code, or None if the URL is invalid
    """
    global _shortener
    if _shortener is None:
        _shortener = URLShortener()
    return _shortener.shorten(url)


def expand_url(short_code: str) -> Optional[str]:
    """Convenience function to expand a short code.
    
    Args:
        short_code: The short code to expand
        
    Returns:
        The original URL, or None if not found
    """
    global _shortener
    if _shortener is None:
        _shortener = URLShortener()
    return _shortener.expand(short_code)


def reset_shortener() -> None:
    """Reset the singleton shortener instance. Useful for testing."""
    global _shortener
    _shortener = None
  