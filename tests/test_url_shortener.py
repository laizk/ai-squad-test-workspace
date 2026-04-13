import pytest
from src.url_shortener import URLShortener, shorten_url, expand_url, reset_shortener


class TestURLShortener:
    """Test cases for URLShortener functionality."""

    def setup_method(self):
        """Reset the singleton before each test."""
        reset_shortener()

    def test_shorten_valid_url(self):
        """Test that a valid URL is shortened correctly."""
        shortener = URLShortener()
        url = "https://www.example.com/very-long-path?query=param"
        short_code = shortener.shorten(url)
        
        assert short_code is not None
        assert len(short_code) == 8
        assert expand_url(short_code) == url

    def test_shorten_invalid_url_no_scheme(self):
        """Test that URLs without http/https scheme return None."""
        shortener = URLShortener()
        short_code = shortener.shorten("example.com")
        
        assert short_code is None

    def test_shorten_empty_url(self):
        """Test that empty URL returns None."""
        shortener = URLShortener()
        short_code = shortener.shorten("")
        
        assert short_code is None

    def test_shorten_none_url(self):
        """Test that None URL returns None."""
        shortener = URLShortener()
        short_code = shortener.shorten(None)
        
        assert short_code is None

    def test_expand_nonexistent_code(self):
        """Test that expanding a non-existent code returns None."""
        shortener = URLShortener()
        result = shortener.expand("abc12345")
        
        assert result is None

    def test_collision_handling(self):
        """Test that multiple URLs get unique short codes."""
        shortener = URLShortener()
        url1 = "https://www.example.com/path1"
        url2 = "https://www.example.com/path2"
        
        code1 = shortener.shorten(url1)
        code2 = shortener.shorten(url2)
        
        assert code1 != code2
        assert expand_url(code1) == url1
        assert expand_url(code2) == url2

    def test_multiple_urls_same_shortener(self):
        """Test that a single URLShortener instance handles multiple URLs."""
        shortener = URLShortener()
        urls = [
            "https://google.com",
            "https://github.com",
            "https://stackoverflow.com",
        ]
        
        codes = [shortener.shorten(url) for url in urls]
        
        assert len(codes) == 3
        assert len(set(codes)) == 3  # All codes should be unique
        
        for url, code in zip(urls, codes):
            assert expand_url(code) == url

    def test_shorten_with_query_params(self):
        """Test shortening URLs with query parameters."""
        shortener = URLShortener()
        url = "https://example.com/search?q=python&lang=en"
        short_code = shortener.shorten(url)
        
        assert short_code is not None
        assert expand_url(short_code) == url

    def test_shorten_with_fragment(self):
        """Test shortening URLs with fragments."""
        shortener = URLShortener()
        url = "https://example.com/page#section"
        short_code = shortener.shorten(url)
        
        assert short_code is not None
        assert expand_url(short_code) == url

    def test_convenience_shorten_url_function(self):
        """Test the convenience shorten_url function."""
        result = shorten_url("https://www.example.com/test")
        
        assert result is not None
        assert expand_url(result) == "https://www.example.com/test"

    def test_convenience_expand_url_function(self):
        """Test the convenience expand_url function."""
        shortener = URLShortener()
        url = "https://www.example.com/test"
        short_code = shortener.shorten(url)
        
        result = expand_url(short_code)
        
        assert result == url

    def test_shorten_with_special_characters(self):
        """Test shortening URLs with special characters."""
        shortener = URLShortener()
        url = "https://example.com/path?foo=bar&baz=qux"
        short_code = shortener.shorten(url)
        
        assert short_code is not None
        assert expand_url(short_code) == url

    def test_shorten_with_port(self):
        """Test shortening URLs with port numbers."""
        shortener = URLShortener()
        url = "https://example.com:8080/path"
        short_code = shortener.shorten(url)
        
        assert short_code is not None
        assert expand_url(short_code) == url

    def test_shorten_with_localhost(self):
        """Test shortening URLs with localhost."""
        shortener = URLShortener()
        url = "http://localhost:3000/api/users"
        short_code = shortener.shorten(url)
        
        assert short_code is not None
        assert expand_url(short_code) == url
  