"""Web browser viewer for ThingsBoard dashboard."""

import logging
from typing import Optional

from PyQt6.QtCore import QUrl
from PyQt6.QtWidgets import QMainWindow
from PyQt6.QtWebEngineWidgets import QWebEngineView
from PyQt6.QtWebEngineCore import QWebEngineProfile, QWebEnginePage

from src.config import AppConfig

logger = logging.getLogger(__name__)


class DashboardViewer(QMainWindow):
    """Main window for displaying ThingsBoard dashboard with visual adjustments.
    
    This viewer embeds a web browser that loads a ThingsBoard dashboard
    and applies custom styling to hide navigation bars and maximize
    the visible dashboard area.
    
    Attributes:
        config: Application configuration settings
        browser: Qt web engine view component
        profile: Browser profile for cookie persistence
    """
    
    def __init__(self, config: AppConfig) -> None:
        """Initialize the dashboard viewer.
        
        Args:
            config: Application configuration object
        """
        super().__init__()
        self.config = config
        
        self._setup_window()
        self._setup_browser()
        self._load_dashboard()
        
        logger.info("Dashboard viewer initialized successfully")
    
    def _setup_window(self) -> None:
        """Configure the main window properties."""
        self.setWindowTitle(self.config.window_title)
        logger.debug(f"Window title set to: {self.config.window_title}")
    
    def _setup_browser(self) -> None:
        """Configure the web browser component with persistent cookies."""
        try:
            self.browser = QWebEngineView()
            
            # Configure profile with persistent cookies
            self.profile = QWebEngineProfile(self.config.profile_name, self.browser)
            self.profile.setPersistentCookiesPolicy(
                QWebEngineProfile.PersistentCookiesPolicy.ForcePersistentCookies
            )
            
            # Create and set the web page with the profile
            web_page = QWebEnginePage(self.profile, self.browser)
            self.browser.setPage(web_page)
            
            # Connect load finished signal to inject visual adjustments
            self.browser.loadFinished.connect(self._inject_visual_adjustments)
            
            self.setCentralWidget(self.browser)
            logger.debug("Browser configured with persistent cookie support")
            
        except Exception as e:
            logger.error(f"Failed to setup browser: {e}", exc_info=True)
            raise
    
    def _load_dashboard(self) -> None:
        """Load the ThingsBoard dashboard URL."""
        try:
            dashboard_url = QUrl(self.config.dashboard_url)
            self.browser.setUrl(dashboard_url)
            logger.info(f"Loading dashboard from: {self.config.dashboard_url}")
            
        except Exception as e:
            logger.error(f"Failed to load dashboard URL: {e}", exc_info=True)
            raise
    
    def _inject_visual_adjustments(self, success: bool) -> None:
        """Inject CSS and JavaScript to hide navigation bars and maximize dashboard.
        
        This method is called when the page finishes loading. It waits for
        the visual elements to load and then applies custom styling to hide
        headers, toolbars, and sidebars.
        
        Args:
            success: Whether the page loaded successfully
        """
        if not success:
            logger.warning("Page load failed, skipping visual adjustments")
            return
        
        try:
            cleanup_script = self._generate_cleanup_script()
            self.browser.page().runJavaScript(cleanup_script)
            logger.info("Visual adjustments injected successfully")
            
        except Exception as e:
            logger.error(f"Failed to inject visual adjustments: {e}", exc_info=True)
    
    def _generate_cleanup_script(self) -> str:
        """Generate the JavaScript code for visual adjustments.
        
        Returns:
            str: JavaScript code to hide navigation elements
        """
        return f"""
        setTimeout(function() {{
            // Create a stylesheet to hide navigation bars
            var style = document.createElement('style');
            style.innerHTML = `
                /* Hide the top green header bar */
                header, .tb-header, mat-toolbar.mat-primary {{ 
                    display: none !important; 
                }}
                
                /* Hide the dashboard title bar (with edit button) */
                .tb-dashboard-toolbar, tb-dashboard-toolbar {{ 
                    display: none !important; 
                }}
                
                /* Hide the sidebar if it appears */
                mat-sidenav {{ 
                    display: none !important; 
                }}
                
                /* Remove extra margins to use full space */
                .mat-drawer-content {{ 
                    margin-left: 0px !important; 
                    height: 100vh !important;
                }}
                
                /* Force dashboard content to fill the screen */
                .tb-dashboard-content {{
                    height: 100vh !important;
                    padding-top: 0px !important;
                }}
            `;
            document.head.appendChild(style);
            
            // Optional: Try to click fullscreen button if it exists
            var buttons = document.querySelectorAll('button mat-icon');
            buttons.forEach(function(icon) {{
                if (icon.innerText === 'fullscreen') {{
                    icon.closest('button').click();
                }}
            }});
            
        }}, {self.config.inject_delay_ms});
        """
