"""Configuration module for the SCADA supervision system."""

import os
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class AppConfig:
    """Application configuration settings.
    
    Attributes:
        dashboard_url: URL of the ThingsBoard dashboard
        window_title: Title of the application window
        profile_name: Name of the browser profile for cookie persistence
        inject_delay_ms: Delay in milliseconds before injecting visual adjustments
    """
    dashboard_url: str
    window_title: str
    profile_name: str
    inject_delay_ms: int


def load_config() -> AppConfig:
    """Load configuration from environment variables with fallback to defaults.
    
    Returns:
        AppConfig: Configuration object with all settings
    """
    return AppConfig(
        dashboard_url=os.getenv(
            "DASHBOARD_URL",
            "https://thingsboard.cloud/dashboards/all/e1a77d10-e83b-11f0-a6fc-1dffa956f056"
        ),
        window_title=os.getenv(
            "WINDOW_TITLE",
            "Sistema de Supervisión - Máquina dosificadora"
        ),
        profile_name=os.getenv("BROWSER_PROFILE", "CacheTesis"),
        inject_delay_ms=int(os.getenv("INJECT_DELAY_MS", "2000"))
    )
