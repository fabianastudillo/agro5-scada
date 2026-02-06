"""
DEPRECATED: This file is kept for backward compatibility.
Please use: python -m src.main
"""

import sys
import warnings

warnings.warn(
    "main.py is deprecated. Use 'python -m src.main' instead.",
    DeprecationWarning,
    stacklevel=2
)

from src.main import main

if __name__ == "__main__":
    sys.exit(main())

