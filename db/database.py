import sqlite3
from threading import Lock

class DatabaseConnection:
    _instance = None
    _lock = Lock()

    def __init__(self, db_path="tickets_table.db"):
        if hasattr(self, "_initialized") and self._initialized:
            return
        self.conn = sqlite3.connect(db_path, check_same_thread=False)
        self._initialized = True
        self._init_db()

    @classmethod
    def get_instance(cls):
        with cls._lock:
            if cls._instance is None:
                cls._instance = cls()
            return cls._instance

    def _init_db(self):
        self.conn.execute("""
            CREATE TABLE IF NOT EXISTS tickets (
                ticket_id TEXT PRIMARY KEY,
                summary TEXT NOT NULL,
                severity TEXT NOT NULL,
                department TEXT NOT NULL,
                category TEXT NOT NULL,
                status TEXT NOT NULL,
                created_at TEXT NOT NULL,
                closed_at TEXT
            )
        """)
        self.conn.commit()

    def get_connection(self):
        return self.conn
