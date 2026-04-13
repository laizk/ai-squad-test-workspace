import uuid
from typing import Dict, Optional


class URLShortener:
    """Minimal URL shortener with in-memory storage."""

    def __init__(self):
        self._store: Dict[str, str] = {}
        self._counter: int = 0

    def shorten(self, url: str) -> str:
        """Shorten a URL and return the short code.

        Args:
            url: The original URL to shorten

        Returns:
            A short code that can be used to retrieve the original URL
        """
        if not url or not isinstance(url, str):
            raise ValueError("URL must be a non-empty string")

        # Generate a short code
        short_code = f"{self._counter:06d}"
        self._counter += 1

        # Store the mapping
        self._store[short_code] = url

        return short_code

    def expand(self, short_code: str) -> Optional[str]:
        """Expand a short code back to the original URL.

        Args:
            short_code: The short code to expand

        Returns:
            The original URL if found, None otherwise
        """
        return self._store.get(short_code)

    def get_store(self) -> Dict[str, str]:
        """Return a copy of the internal store for inspection."""
        return dict(self._store)

    def clear(self) -> None:
        """Clear all stored URLs."""
        self._store.clear()
        self._counter = 0


# Singleton instance for convenience functions to share state
_shortener = URLShortener()


def shorten_url(url: str) -> str:
    """Convenience function to shorten a URL.

    Args:
        url: The original URL to shorten

    Returns:
        A short code
    """
    return _shortener.shorten(url)


def expand_url(short_code: str) -> Optional[str]:
    """Convenience function to expand a short code.

    Args:
        short_code: The short code to expand

    Returns:
        The original URL or None if not found
    """
    return _shortener.expand(short_code)


def clear_store() -> None:
    """Convenience function to clear the store."""
    _shortener.clear()
  