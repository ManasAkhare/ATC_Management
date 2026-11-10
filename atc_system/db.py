"""
Database Manager for PostgreSQL.
Provides connection pooling, role context management, and query helpers.
"""

import psycopg2
from psycopg2 import extras
from atc_system.config import Config

class DatabaseManager:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(DatabaseManager, cls).__new__(cls)
            cls._instance.connection = None
            cls._instance.active_role = "postgres"
        return cls._instance

    def get_connection(self):
        """Returns an active connection or creates a new one."""
        if self.connection is None or self.connection.closed:
            self.connect()
        return self.connection

    def connect(self):
        """Establishes connection to PostgreSQL using Config."""
        try:
            self.connection = psycopg2.connect(**Config.get_dsn())
            self.connection.autocommit = True
            
            # Reapply role if not postgres
            if self.active_role and self.active_role != "postgres":
                with self.connection.cursor() as cur:
                    cur.execute(f"SET ROLE {self.active_role};")
            return True, "Connected successfully."
        except Exception as e:
            self.connection = None
            return False, str(e)

    def is_connected(self):
        """Checks if current connection is alive."""
        if self.connection is None or self.connection.closed:
            return False
        try:
            with self.connection.cursor() as cur:
                cur.execute("SELECT 1;")
            return True
        except Exception:
            return False

    def close(self):
        """Closes the active database connection."""
        if self.connection and not self.connection.closed:
            self.connection.close()
        self.connection = None

    def set_role(self, role_name: str):
        """Switches the PostgreSQL session role for RLS / RBAC demo."""
        conn = self.get_connection()
        try:
            with conn.cursor() as cur:
                if role_name.lower() in ("postgres", "reset", "none"):
                    cur.execute("RESET ROLE;")
                    self.active_role = "postgres"
                else:
                    cur.execute(f"SET ROLE {role_name};")
                    self.active_role = role_name
            return True, f"Session role changed to '{self.active_role}'."
        except Exception as e:
            return False, f"Failed to set role '{role_name}': {e}"

    def get_current_role(self):
        """Fetches CURRENT_USER / SESSION_USER from PostgreSQL."""
        try:
            rows, _ = self.execute_query("SELECT CURRENT_USER, SESSION_USER;")
            if rows:
                return rows[0][0]
        except Exception:
            pass
        return self.active_role

    def execute_query(self, query: str, params=None, fetch=True):
        """
        Executes a SQL query and returns (rows, column_names).
        """
        conn = self.get_connection()
        with conn.cursor() as cur:
            cur.execute(query, params or ())
            if fetch and cur.description:
                cols = [desc[0] for desc in cur.description]
                rows = cur.fetchall()
                return rows, cols
            return [], []

    def execute_non_query(self, query: str, params=None):
        """
        Executes INSERT/UPDATE/DELETE and returns affected row count.
        """
        conn = self.get_connection()
        with conn.cursor() as cur:
            cur.execute(query, params or ())
            return cur.rowcount

db_manager = DatabaseManager()
