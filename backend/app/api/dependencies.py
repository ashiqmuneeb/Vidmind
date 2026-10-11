from typing import AsyncGenerator
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from backend.app.db.database import get_db

# Re-export get_db for cleaner route imports
DatabaseSession = Depends(get_db)
