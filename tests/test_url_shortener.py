import pytest
from src.url_shortener import URLShortener, shorten_url, expand_url, clear_store


class TestURLShortenerBasicFunctionality:
    """Tests for basic URL shortening functionality."""
    
    def test_shorten_url_returns_short_code(self):
        """Test that shortening a URL returns a short code."""
        shortener = URLShortener()
        original_url = "https://example.com/very/long/path/to/resource"
        short_code = shortener.shorten_url(original_url)
        
        assert isinstance(short_code, str)
        assert len(short_code) == 6
        assert short_code != original_url
    
    def test_expand_url_returns_original(self):
        """Test that expanding a short code returns the original URL."""
        shortener = URLShortener()
        original_url = "https://example.com/path"
        short_code = shortener.shorten_url(original_url)
        expanded = shortener.expand_url(short_code)
        
        assert expanded == original_url
    
    def test_clear_store_removes_all_mappings(self):
        """Test that clear_store removes all URL mappings."""
        shortener = URLShortener()
        shortener.shorten_url("https://example.com/path1")
        shortener.shorten_url("https://example.com/path2")
        shortener.clear_store()
        
        assert shortener.expand_url("any_code") is None


class TestURLShortenerDuplicateHandling:
    """Tests for duplicate URL shortening and unique code generation."""
    
    def test_same_url_gets_different_codes(self):
        """Test that the same URL shortened multiple times gets unique codes."""
        shortener = URLShortener()
        url = "https://example.com/path"
        
        code1 = shortener.shorten_url(url)
        code2 = shortener.shorten_url(url)
        code3 = shortener.shorten_url(url)
        
        assert code1 != code2
        assert code2 != code3
        assert code1 != code3
    
    def test_counter_increments_across_operations(self):
        """Test that the counter properly increments across multiple shorten operations."""
        shortener = URLShortener()
        
        # Shorten multiple URLs
        for i in range(10):
            shortener.shorten_url(f"https://example.com/path{i}")
        
        # Verify we have 10 entries
        assert len(shortener._store) == 10
    
    def test_clear_store_resets_counter(self):
        """Test that clear_store resets the counter."""
        shortener = URLShortener()
        shortener.shorten_url("https://example.com/path1")
        shortener.shorten_url("https://example.com/path2")
        
        assert len(shortener._store) == 2
        
        shortener.clear_store()
        
        assert len(shortener._store) == 0


class TestURLShortenerErrorHandling:
    """Tests for error handling and edge cases."""
    
    def test_shorten_url_empty_string_error(self):
        """Test that empty string raises ValueError."""
        shortener = URLShortener()
        with pytest.raises(ValueError, match="cannot be empty"):
            shortener.shorten_url("")
    
    def test_shorten_url_none_error(self):
        """Test that None raises ValueError."""
        shortener = URLShortener()
        with pytest.raises(ValueError, match="cannot be empty"):
            shortener.shorten_url(None)
    
    def test_shorten_url_invalid_format_error(self):
        """Test that malformed URLs raise ValueError."""
        shortener = URLShortener()
        
        # Test URLs without scheme
        with pytest.raises(ValueError):
            shortener.shorten_url("example.com/path")
        
        # Test URLs without netloc
        with pytest.raises(ValueError):
            shortener.shorten_url("/path/to/resource")
        
        # Test URLs with only scheme
        with pytest.raises(ValueError):
            shortener.shorten_url("http://")
    
    def test_expand_url_empty_code_error(self):
        """Test that empty short code raises ValueError."""
        shortener = URLShortener()
        with pytest.raises(ValueError, match="cannot be empty"):
            shortener.expand_url("")
    
    def test_expand_url_none_error(self):
        """Test that None short code raises ValueError."""
        shortener = URLShortener()
        with pytest.raises(ValueError, match="cannot be empty"):
            shortener.expand_url(None)


class TestURLShortenerEdgeCases:
    """Tests for edge cases and special characters."""
    
    def test_shorten_url_with_special_characters(self):
        """Test shortening URLs with special characters."""
        shortener = URLShortener()
        url = "https://example.com/path?query=param&other=value#section"
        short_code = shortener.shorten_url(url)
        expanded = shortener.expand_url(short_code)
        
        assert expanded == url
    
    def test_shorten_url_with_unicode(self):
        """Test shortening URLs with unicode characters."""
        shortener = URLShortener()
        url = "https://example.com/path?name=日本語"
        short_code = shortener.shorten_url(url)
        expanded = shortener.expand_url(short_code)
        
        assert expanded == url
    
    def test_shorten_url_with_very_long_url(self):
        """Test shortening very long URLs."""
        shortener = URLShortener()
        long_url = "https://example.com/" + "a" * 10000
        short_code = shortener.shorten_url(long_url)
        expanded = shortener.expand_url(short_code)
        
        assert expanded == long_url
    
    def test_shorten_url_with_special_schemes(self):
        """Test shortening URLs with different schemes."""
        shortener = URLShortener()
        
        schemes = [
            "https://example.com/path",
            "http://example.com/path",
            "ftp://example.com/path",
        ]
        
        for url in schemes:
            short_code = shortener.shorten_url(url)
            expanded = shortener.expand_url(short_code)
            assert expanded == url


class TestURLShortenerConvenienceFunctions:
    """Tests for convenience functions."""
    
    def test_shorten_url_convenience_function(self):
        """Test the shorten_url convenience function."""
        original_url = "https://example.com/path"
        short_code = shorten_url(original_url)
        
        assert isinstance(short_code, str)
        assert len(short_code) == 6
    
    def test_expand_url_convenience_function(self):
        """Test the expand_url convenience function."""
        shortener = URLShortener()
        original_url = "https://example.com/path"
        short_code = shortener.shorten_url(original_url)
        
        expanded = expand_url(short_code)
        assert expanded == original_url
    
    def test_clear_store_convenience_function(self):
        """Test the clear_store convenience function."""
        shortener = URLShortener()
        shortener.shorten_url("https://example.com/path1")
        
        clear_store(shortener)
        
        assert shortener.expand_url("any_code") is None
    
    def test_convenience_functions_with_new_instance(self):
        """Test that convenience functions work with new instances."""
        # Each call creates a new instance
        code1 = shorten_url("https://example.com/path1")
        code2 = shorten_url("https://example.com/path2")
        
        # They should be different because they use different instances
        assert code1 != code2


class TestURLShortenerIsolation:
    """Tests for test isolation - each test uses its own instance."""
    
    def test_isolation_first(self):
        """First isolation test."""
        shortener = URLShortener()
        code = shortener.shorten_url("https://example.com/path")
        assert len(code) == 6
    
    def test_isolation_second(self):
        """Second isolation test - should not be affected by first."""
        shortener = URLShortener()
        code = shortener.shorten_url("https://example.com/path")
        assert len(code) == 6
        assert shortener.expand_url(code) == "https://example.com/path"
    
    def test_isolation_third(self):
        """Third isolation test - should have empty store."""
        shortener = URLShortener()
        assert len(shortener._store) == 0
        assert shortener.expand_url("any_code") is None
