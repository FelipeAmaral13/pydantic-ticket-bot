from dataclasses import dataclass, field
from db.database import DatabaseConnection
import sqlite3

@dataclass
class State:
    summary: str = ""
    severity: str = ""
    department: str = ""
    category: str = ""
    ticket_id: str = ""
    status: str = ""
    created_at: str = "" 
    closed_at: str = "" 
    db: sqlite3.Connection = field(
        default_factory=lambda: DatabaseConnection.get_instance().get_connection()
    )