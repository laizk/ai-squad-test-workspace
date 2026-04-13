import pytest
from url_shortener import URLShortener, shorten_url, expand_url


class TestURLShortener:
    """Test suite for URLShortener."""
    
    def setup_method(self):
        """Reset storage before each test."""
        URLShortener.reset()
    
    def test_shorten_valid_url(self):
        """Test shortening a valid URL."""
        url = "https://www.example.com/very-long-path?query=param"
        short_code = shorten_url(url)
        
        assert short_code is not None
        assert len(short_code) == 8
        assert expand_url(short_code) == url
    
    def test_shorten_different_urls(self):
        """Test that different URLs get different short codes."""
        url1 = "https://www.example.com/path1"
        url2 = "https://www.example.com/path2"
        
        code1 = shorten_url(url1)
        code2 = shorten_url(url2)
        
        assert code1 != code2
        assert expand_url(code1) == url1
        assert expand_url(code2) == url2
    
    def test_collision_handling(self):
        """Test that collisions are handled correctly."""
        url1 = "https://www.example.com/path1"
        url2 = "https://www.example.com/path2"
        
        code1 = shorten_url(url1)
        code2 = shorten_url(url2)
        
        # First URL should still resolve correctly
        assert expand_url(code1) == url1
        assert expand_url(code2) == url2
    
    def test_multiple_urls_same_shortener(self):
        """Test multiple URLs with the same shortener instance."""
        url1 = "https://google.com"
        url2 = "https://github.com"
        
        code1 = shorten_url(url1)
        code2 = shorten_url(url2)
        
        assert expand_url(code1) == url1
        assert expand_url(code2) == url2
    
    def test_shorten_with_query_params(self):
        """Test shortening URL with query parameters."""
        url = "https://example.com/search?q=python&lang=en"
        short_code = shorten_url(url)
        
        assert expand_url(short_code) == url
    
    def test_shorten_with_fragment(self):
        """Test shortening URL with fragment."""
        url = "https://example.com/page#section"
        short_code = shorten_url(url)
        
        assert expand_url(short_code) == url
    
    def test_shorten_with_special_characters(self):
        """Test shortening URL with special characters."""
        url = "https://example.com/path?foo=bar&baz=qux"
        short_code = shorten_url(url)
        
        assert expand_url(short_code) == url
    
    def test_shorten_with_unicode(self):
        """Test shortening URL with unicode characters."""
        url = "https://example.com/path?name=日本語"
        short_code = shorten_url(url)
        
        assert expand_url(short_code) == url
    
    def test_convenience_expand_url_function(self):
        """Test the convenience expand_url function."""
        url = "https://www.example.com/test"
        short_code = shorten_url(url)
        
        result = expand_url(short_code)
        assert result == url
    
    def test_shorten_empty_string(self):
        """Test shortening an empty string URL."""
        url = ""
        short_code = shorten_url(url)
        
        assert expand_url(short_code) == url
    
    def test_shorten_very_long_url(self):
        """Test shortening a very long URL."""
        long_url = "https://example.com/" + "a" * 10000
        short_code = shorten_url(long_url)
        
        assert expand_url(short_code) == long_url
    
    def test_shorten_with_port(self):
        """Test shortening URL with port number."""
        url = "https://example.com:8080/path"
        short_code = shorten_url(url)
        
        assert expand_url(short_code) == url
    
    def test_shorten_with_subdomain(self):
        """Test shortening URL with subdomain."""
        url = "https://sub.example.com/path"
        short_code = shorten_url(url)
        
        assert expand_url(short_code) == url
