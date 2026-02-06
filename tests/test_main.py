"""Test main module."""

import sys
from unittest.mock import Mock, patch, MagicMock
import pytest

from src.main import setup_logging, main


class TestSetupLogging:
    """Test suite for setup_logging function."""
    
    @patch('logging.basicConfig')
    def test_setup_logging_configures_correctly(self, mock_basic_config):
        """Test that logging is configured with correct parameters."""
        setup_logging()
        
        mock_basic_config.assert_called_once()
        call_kwargs = mock_basic_config.call_args[1]
        
        assert 'level' in call_kwargs
        assert 'format' in call_kwargs
        assert 'datefmt' in call_kwargs
        assert 'name' in call_kwargs['format']
        assert 'levelname' in call_kwargs['format']


class TestMain:
    """Test suite for main function."""
    
    @patch('src.main.QApplication')
    @patch('src.main.DashboardViewer')
    @patch('src.main.load_config')
    def test_main_successful_execution(self, mock_load_config, mock_viewer, mock_qapp):
        """Test successful execution of main function."""
        # Setup mocks
        mock_config = Mock()
        mock_load_config.return_value = mock_config
        
        mock_app_instance = Mock()
        mock_app_instance.exec.return_value = 0
        mock_qapp.return_value = mock_app_instance
        
        mock_window = Mock()
        mock_viewer.return_value = mock_window
        
        # Execute main
        exit_code = main()
        
        # Verify calls
        mock_load_config.assert_called_once()
        mock_qapp.assert_called_once()
        mock_viewer.assert_called_once_with(mock_config)
        mock_window.showMaximized.assert_called_once()
        mock_app_instance.exec.assert_called_once()
        
        assert exit_code == 0
    
    @patch('src.main.QApplication')
    @patch('src.main.load_config')
    def test_main_handles_config_error(self, mock_load_config, mock_qapp):
        """Test that main handles configuration errors gracefully."""
        mock_load_config.side_effect = Exception("Config error")
        
        exit_code = main()
        
        assert exit_code == 1
    
    @patch('src.main.QApplication')
    @patch('src.main.DashboardViewer')
    @patch('src.main.load_config')
    def test_main_handles_viewer_error(self, mock_load_config, mock_viewer, mock_qapp):
        """Test that main handles viewer initialization errors."""
        mock_config = Mock()
        mock_load_config.return_value = mock_config
        mock_viewer.side_effect = Exception("Viewer error")
        
        exit_code = main()
        
        assert exit_code == 1
    
    @patch('src.main.QApplication')
    @patch('src.main.DashboardViewer')
    @patch('src.main.load_config')
    def test_main_returns_app_exit_code(self, mock_load_config, mock_viewer, mock_qapp):
        """Test that main returns the application exit code."""
        mock_config = Mock()
        mock_load_config.return_value = mock_config
        
        mock_app_instance = Mock()
        mock_app_instance.exec.return_value = 42
        mock_qapp.return_value = mock_app_instance
        
        mock_window = Mock()
        mock_viewer.return_value = mock_window
        
        exit_code = main()
        
        assert exit_code == 42
