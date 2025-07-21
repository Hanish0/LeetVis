"""
Database package for LeetCode Video Generator.
Contains all database-related functionality including client, service, and initialization.
"""

from .client import db_client, VIDEOS_TABLE, PROBLEMS_TABLE
from .service import DatabaseService

__all__ = ['db_client', 'VIDEOS_TABLE', 'PROBLEMS_TABLE', 'DatabaseService']