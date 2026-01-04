#!/usr/bin/env python3
"""Initialize the database and create all tables."""

import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from crystaldb.core.logging import setup_logging, get_logger
from crystaldb.db import init_db

setup_logging()
logger = get_logger(__name__)


def main() -> None:
    """Initialize the database."""
    try:
        logger.info("Initializing database...")
        init_db()
        logger.info("Database initialized successfully!")
    except Exception as e:
        logger.error(f"Failed to initialize database: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
