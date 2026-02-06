# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] - 2026-02-06

### Added
- Modular architecture with separation of concerns (config, viewer, main)
- Type hints on all functions and classes
- Google-style docstrings for all public APIs
- Structured logging with appropriate levels (INFO, DEBUG, ERROR)
- Configuration management via environment variables
- Comprehensive unit tests with >85% coverage
- Error handling with try/except and logging
- CI/CD workflow with GitHub Actions
- Code quality tools configuration (flake8, mypy, bandit)
- Security best practices implementation
- Proper .gitignore for Python projects
- Updated README with installation and usage instructions
- **build.sh script for automated binary generation (Windows/Linux)**
- **GitHub Actions workflow for automated cross-platform builds**
- **Automatic Release creation with binaries when tagging versions**
- Documentation for GitHub Actions usage

### Changed
- Refactored main.py to follow Clean Code and SOLID principles
- Renamed all Spanish variables/functions/classes to English
- Moved from monolithic script to modular src/ structure
- Replaced inline comments with structured logging
- Extracted hardcoded configuration to config.py
- Updated requirements.txt with version pinning and dev dependencies

### Deprecated
- Old main.py (kept for backward compatibility with deprecation warning)

## [0.1.0] - Initial Release

### Added
- Basic PyQt6 web viewer for ThingsBoard dashboard
- Cookie persistence support
- Visual adjustments injection to hide navigation bars
- PyInstaller spec file for executable generation
