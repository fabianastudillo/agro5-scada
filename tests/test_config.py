"""Test configuration module."""

import os
import pytest

from src.config import AppConfig, load_config


class TestAppConfig:
    """Test suite for AppConfig dataclass."""
    
    def test_app_config_creation(self):
        """Test that AppConfig can be created with valid parameters."""
        config = AppConfig(
            dashboard_url="https://example.com/dashboard",
            window_title="Test Window",
            profile_name="TestProfile",
            inject_delay_ms=3000
        )
        
        assert config.dashboard_url == "https://example.com/dashboard"
        assert config.window_title == "Test Window"
        assert config.profile_name == "TestProfile"
        assert config.inject_delay_ms == 3000
    
    def test_app_config_is_frozen(self):
        """Test that AppConfig is immutable (frozen dataclass)."""
        config = AppConfig(
            dashboard_url="https://example.com",
            window_title="Test",
            profile_name="Profile",
            inject_delay_ms=2000
        )
        
        with pytest.raises(AttributeError):
            config.dashboard_url = "https://new-url.com"


class TestLoadConfig:
    """Test suite for load_config function."""
    
    def test_load_config_with_defaults(self, monkeypatch):
        """Test loading configuration with default values."""
        # Clear any existing environment variables
        monkeypatch.delenv("DASHBOARD_URL", raising=False)
        monkeypatch.delenv("WINDOW_TITLE", raising=False)
        monkeypatch.delenv("BROWSER_PROFILE", raising=False)
        monkeypatch.delenv("INJECT_DELAY_MS", raising=False)
        
        config = load_config()
        
        assert "thingsboard.cloud" in config.dashboard_url
        assert "Máquina dosificadora" in config.window_title
        assert config.profile_name == "CacheTesis"
        assert config.inject_delay_ms == 2000
    
    def test_load_config_from_environment(self, monkeypatch):
        """Test loading configuration from environment variables."""
        monkeypatch.setenv("DASHBOARD_URL", "https://custom.url/dashboard")
        monkeypatch.setenv("WINDOW_TITLE", "Custom Title")
        monkeypatch.setenv("BROWSER_PROFILE", "CustomProfile")
        monkeypatch.setenv("INJECT_DELAY_MS", "5000")
        
        config = load_config()
        
        assert config.dashboard_url == "https://custom.url/dashboard"
        assert config.window_title == "Custom Title"
        assert config.profile_name == "CustomProfile"
        assert config.inject_delay_ms == 5000
    
    def test_load_config_partial_environment(self, monkeypatch):
        """Test loading configuration with some env vars and some defaults."""
        monkeypatch.delenv("DASHBOARD_URL", raising=False)
        monkeypatch.delenv("BROWSER_PROFILE", raising=False)
        monkeypatch.setenv("WINDOW_TITLE", "Partial Config")
        monkeypatch.setenv("INJECT_DELAY_MS", "3000")
        
        config = load_config()
        
        assert "thingsboard.cloud" in config.dashboard_url
        assert config.window_title == "Partial Config"
        assert config.profile_name == "CacheTesis"
        assert config.inject_delay_ms == 3000
    
    def test_load_config_invalid_delay_uses_default(self, monkeypatch):
        """Test that invalid INJECT_DELAY_MS falls back to default."""
        monkeypatch.setenv("INJECT_DELAY_MS", "invalid")
        
        with pytest.raises(ValueError):
            load_config()
