"""
VidMind Database Initialization Script
Creates all tables in SQLite/PostgreSQL using SQLAlchemy models.
"""
import asyncio
import sys
import os

# Ensure backend is on sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from backend.app.db.database import init_db
from backend.app.core.logging import logger, setup_logging


async def main():
    setup_logging()
    logger.info("Initializing VidMind database schema...")
    try:
        await init_db()
        print("[+] All database tables created successfully.")
    except Exception as e:
        logger.error(f"Failed to initialize database: {e}")
        sys.exit(1)


if __name__ == "__main__":
    asyncio.run(main())
