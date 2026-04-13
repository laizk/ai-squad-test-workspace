import pytest
from src.url_shortener import URLShortener, shorten_url, expand_url


class TestURLShortener:
    """Tests for the URLShortener class."""

    def test_shorten_url(self):
        """Test that a URL can be shortened."""
        shortener = URLShortener()
        original_url = "https://example.com/very/long/path?query=param"
        short_code = shortener.shorten(original_url)

        assert short_code is not None
        assert len(short_code) > 0

    def test_expand_url(self):
        """Test that a short code can be expanded back to the original URL."""
        shortener = URLShortener()
        original_url = "https://example.com/very/long/path?query=param"
        short_code = shortener.shorten(original_url)
        expanded_url = shortener.expand(short_code)

        assert expanded_url == original_url

    def test_shorten_different_urls(self):
        """Test that different URLs get different short codes."""
        shortener = URLShortener()
        url1 = "https://example.com/path1"
        url2 = "https://example.com/path2"

        code1 = shortener.shorten(url1)
        code2 = shortener.shorten(url2)

        assert code1 != code2

    def test_expand_nonexistent_code(self):
        """Test that expanding a non-existent code returns None."""
        shortener = URLShortener()
        result = shortener.expand("999999")

        assert result is None

    def test_clear_store(self):
        """Test that clearing the store removes all URLs."""
        shortener = URLShortener()
        shortener.shorten("https://example.com/test")
        shortener.clear()

        result = shortener.expand("000000")
        assert result is None

    def test_shorten_convenience_function(self):
        """Test the shorten_url convenience function."""
        short_code = shorten_url("https://example.com/test")

        assert short_code is not None
        assert len(short_code) > 0

    def test_expand_convenience_function(self):
        """Test the expand_url convenience function."""
        short_code = shorten_url("https://example.com/test")
        expanded = expand_url(short_code)

        assert expanded == "https://example.com/test"

    def test_invalid_url_raises_error(self):
        """Test that invalid URLs raise ValueError."""
        shortener = URLShortener()

        with pytest.raises(ValueError):
            shortener.shorten("")

        with pytest.raises(ValueError):
            shortener.shorten(None)

    def test_multiple_shortens_same_shortener(self):
        """Test that multiple shortens work on the same instance."""
        shortener = URLShortener()
        code1 = shortener.shorten("https://example.com/1")
        code2 = shortener.shorten("https://example.com/2")
        code3 = shortener.shorten("https://example.com/3")

        assert code1 != code2
        assert code2 != code3
        assert code1 != code3

        # Verify all can be expanded
        assert shortener.expand(code1) == "https://example.com/1"
        assert shortener.expand(code2) == "https://example.com/2"
        assert shortener.expand(code3) == "https://example.com/3"
  