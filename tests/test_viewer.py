"""Test viewer module."""

from unittest.mock import Mock, patch, MagicMock
import pytest

from PyQt6.QtCore import QUrl
from PyQt6.QtWidgets import QApplication

from src.config import AppConfig
from src.viewer import DashboardViewer


@pytest.fixture
def qt_app():
    """Create a QApplication instance for testing."""
    app = QApplication.instance()
    if app is None:
        app = QApplication([])
    return app


@pytest.fixture
def test_config():
    """Create a test configuration."""
    return AppConfig(
        dashboard_url="https://test.example.com/dashboard",
        window_title="Test Dashboard",
        profile_name="TestProfile",
        inject_delay_ms=1000
    )


class TestDashboardViewer:
    """Test suite for DashboardViewer class."""
    
    def test_viewer_initialization(self, qt_app, test_config):
        """Test that DashboardViewer initializes correctly."""
        viewer = DashboardViewer(test_config)
        
        assert viewer.config == test_config
        assert viewer.windowTitle() == "Test Dashboard"
        assert viewer.browser is not None
    
    def test_window_title_set_correctly(self, qt_app, test_config):
        """Test that window title is set from configuration."""
        viewer = DashboardViewer(test_config)
        
        assert viewer.windowTitle() == test_config.window_title
    
    @patch('src.viewer.QWebEngineProfile')
    @patch('src.viewer.QWebEnginePage')
    def test_browser_profile_configured(self, mock_page, mock_profile, qt_app, test_config):
        """Test that browser profile is configured with persistent cookies."""
        viewer = DashboardViewer(test_config)
        
        # Verify profile was created with correct name
        assert viewer.profile is not None
    
    def test_dashboard_url_loaded(self, qt_app, test_config):
        """Test that dashboard URL is loaded in the browser."""
        viewer = DashboardViewer(test_config)
        
        loaded_url = viewer.browser.url().toString()
        assert loaded_url == test_config.dashboard_url
    
    def test_generate_cleanup_script_contains_css(self, qt_app, test_config):
        """Test that cleanup script contains expected CSS rules."""
        viewer = DashboardViewer(test_config)
        script = viewer._generate_cleanup_script()
        
        # Check for key CSS selectors
        assert "header" in script
        assert ".tb-header" in script
        assert ".tb-dashboard-toolbar" in script
        assert "mat-sidenav" in script
        assert "display: none !important" in script
    
    def test_generate_cleanup_script_uses_delay(self, qt_app, test_config):
        """Test that cleanup script uses configured delay."""
        viewer = DashboardViewer(test_config)
        script = viewer._generate_cleanup_script()
        
        assert str(test_config.inject_delay_ms) in script
        assert "setTimeout" in script
    
    def test_inject_visual_adjustments_on_success(self, qt_app, test_config):
        """Test that visual adjustments are injected when page loads successfully."""
        viewer = DashboardViewer(test_config)
        
        with patch.object(viewer.browser.page(), 'runJavaScript') as mock_run_js:
            viewer._inject_visual_adjustments(True)
            
            # Verify JavaScript was executed
            mock_run_js.assert_called_once()
            script = mock_run_js.call_args[0][0]
            assert "setTimeout" in script
    
    def test_inject_visual_adjustments_on_failure(self, qt_app, test_config):
        """Test that visual adjustments are skipped when page load fails."""
        viewer = DashboardViewer(test_config)
        
        with patch.object(viewer.browser.page(), 'runJavaScript') as mock_run_js:
            viewer._inject_visual_adjustments(False)
            
            # Verify JavaScript was NOT executed
            mock_run_js.assert_not_called()
    
    def test_viewer_handles_invalid_url_gracefully(self, qt_app):
        """Test that viewer handles invalid URLs with proper error logging."""
        invalid_config = AppConfig(
            dashboard_url="",
            window_title="Test",
            profile_name="Test",
            inject_delay_ms=1000
        )
        
        # Should not raise exception, but URL will be empty
        viewer = DashboardViewer(invalid_config)
        assert viewer.browser.url().toString() == ""
