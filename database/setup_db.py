"""
Database Setup Script for Air Traffic Control (ATC) Management System.
Executes database/schema.sql to set up the Airport database in PostgreSQL.
"""

import os
import sys
import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
from dotenv import load_dotenv

# Load credentials from .env or use defaults
load_dotenv()

DB_HOST = os.getenv("DB_HOST", "127.0.0.1")
DB_PORT = int(os.getenv("DB_PORT", "5432"))
DB_USER = os.getenv("DB_USER", "postgres")
DB_PASSWORD = os.getenv("DB_PASSWORD", "#1123581321Slay")
DB_NAME = os.getenv("DB_NAME", "Airport")

def setup_database():
    print("=" * 60)
    print("ATC MANAGEMENT SYSTEM - DATABASE INITIALIZER")
    print("=" * 60)
    print(f"Connecting to PostgreSQL server at {DB_HOST}:{DB_PORT} as '{DB_USER}'...")

    try:
        # Step 1: Connect to maintenance db to check/create target database
        conn = psycopg2.connect(
            host=DB_HOST,
            port=DB_PORT,
            user=DB_USER,
            password=DB_PASSWORD,
            dbname="postgres"
        )
        conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        cur = conn.cursor()

        cur.execute("SELECT 1 FROM pg_database WHERE datname = %s;", (DB_NAME,))
        exists = cur.fetchone()
        if not exists:
            print(f"Creating database '{DB_NAME}'...")
            cur.execute(f'CREATE DATABASE "{DB_NAME}";')
            print(f"Database '{DB_NAME}' created successfully.")
        else:
            print(f"Database '{DB_NAME}' already exists.")

        cur.close()
        conn.close()

        # Step 2: Connect to target database and apply schema
        print(f"Connecting to database '{DB_NAME}'...")
        conn_target = psycopg2.connect(
            host=DB_HOST,
            port=DB_PORT,
            user=DB_USER,
            password=DB_PASSWORD,
            dbname=DB_NAME
        )
        cur_target = conn_target.cursor()

        schema_file = os.path.join(os.path.dirname(__file__), "schema.sql")
        if not os.path.exists(schema_file):
            print(f"Error: Schema file '{schema_file}' not found.")
            return False

        print(f"Executing schema script: {schema_file}...")
        with open(schema_file, "r", encoding="utf-8") as f:
            sql_script = f.read()

        cur_target.execute(sql_script)
        conn_target.commit()

        # Also create adbms roles if not present
        roles_script = """
        DO $$
        BEGIN
            IF NOT EXISTS (SELECT FROM pg_roles WHERE rolname = 'admin') THEN
                CREATE ROLE admin;
            END IF;
            IF NOT EXISTS (SELECT FROM pg_roles WHERE rolname = 'atc') THEN
                CREATE ROLE atc;
            END IF;
            IF NOT EXISTS (SELECT FROM pg_roles WHERE rolname = 'passenger') THEN
                CREATE ROLE passenger;
            END IF;
            IF NOT EXISTS (SELECT FROM pg_roles WHERE rolname = 'captain') THEN
                CREATE ROLE captain WITH PASSWORD '123' LOGIN;
            END IF;
            IF NOT EXISTS (SELECT FROM pg_roles WHERE rolname = 'aditya') THEN
                CREATE ROLE aditya WITH PASSWORD '123' LOGIN IN ROLE passenger;
            END IF;
            IF NOT EXISTS (SELECT FROM pg_roles WHERE rolname = 'parth') THEN
                CREATE ROLE parth WITH PASSWORD '123' LOGIN IN ROLE passenger;
            END IF;
        END $$;
        """
        try:
            cur_target.execute(roles_script)
            conn_target.commit()
            print("Verified security roles (admin, atc, passenger, captain, aditya, parth).")
        except Exception as e:
            print(f"Note on roles setup: {e}")
            conn_target.rollback()

        cur_target.close()
        conn_target.close()

        print("\nDatabase setup completed successfully!")
        print(f"You can now launch the application by running: python run.py")
        return True

    except Exception as e:
        print(f"\nFailed to set up database: {e}")
        print("\nPlease check:")
        print("1. Is PostgreSQL running on localhost:5432?")
        print("2. Are the username and password correct in your .env file?")
        return False

if __name__ == "__main__":
    setup_database()
