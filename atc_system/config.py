"""
Configuration and Environment settings for ATC Management System.
"""

import os
from pathlib import Path
from dotenv import load_dotenv

# Base directory of project
BASE_DIR = Path(__file__).resolve().parent.parent

# Load .env if present
load_dotenv(BASE_DIR / ".env")

class Config:
    DB_HOST: str = os.getenv("DB_HOST", "127.0.0.1")
    DB_PORT: int = int(os.getenv("DB_PORT", "5432"))
    DB_NAME: str = os.getenv("DB_NAME", "Airport")
    DB_USER: str = os.getenv("DB_USER", "postgres")
    DB_PASSWORD: str = os.getenv("DB_PASSWORD", "#1123581321Slay")
    
    # Active role for RLS / security simulation
    CURRENT_ROLE: str = "postgres"
    
    @classmethod
    def update_connection(cls, host, port, dbname, user, password):
        cls.DB_HOST = host
        cls.DB_PORT = int(port)
        cls.DB_NAME = dbname
        cls.DB_USER = user
        cls.DB_PASSWORD = password

    @classmethod
    def get_dsn(cls):
        return {
            "host": cls.DB_HOST,
            "port": cls.DB_PORT,
            "dbname": cls.DB_NAME,
            "user": cls.DB_USER,
            "password": cls.DB_PASSWORD,
            "connect_timeout": 5
        }
