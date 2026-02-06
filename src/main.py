"""Main entry point for the SCADA supervision system."""

import sys
import logging
from pathlib import Path

from PyQt6.QtWidgets import QApplication

from src.config import load_config
from src.viewer import DashboardViewer


def setup_logging() -> None:
    """Configure logging with appropriate format and level."""
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )


def main() -> int:
    """Initialize and run the SCADA supervision application.
    
    Returns:
        int: Application exit code (0 for success, non-zero for errors)
    """
    setup_logging()
    logger = logging.getLogger(__name__)
    
    try:
        logger.info("Starting SCADA supervision system")
        
        # Load configuration
        config = load_config()
        logger.debug(f"Configuration loaded: {config}")
        
        # Create Qt application
        app = QApplication(sys.argv)
        
        # Create and show main window
        window = DashboardViewer(config)
        window.showMaximized()
        logger.info("Application window displayed")
        
        # Run application event loop
        exit_code = app.exec()
        logger.info(f"Application exiting with code: {exit_code}")
        return exit_code
        
    except Exception as e:
        logger.critical(f"Fatal error in main: {e}", exc_info=True)
        return 1


if __name__ == "__main__":
    sys.exit(main())
