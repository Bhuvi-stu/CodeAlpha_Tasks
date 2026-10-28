"""SQLite persistence helpers using parameterized SQL."""
import sqlite3
from contextlib import closing


def initialize_database(database_path):
    with closing(sqlite3.connect(database_path)) as connection:
        connection.execute(
            "CREATE TABLE IF NOT EXISTS users ("
            "id INTEGER PRIMARY KEY AUTOINCREMENT, "
            "username TEXT NOT NULL UNIQUE, password_hash TEXT NOT NULL)"
        )
        connection.commit()


def get_user_by_username(database_path, username):
    with closing(sqlite3.connect(database_path)) as connection:
        connection.row_factory = sqlite3.Row
        return connection.execute(
            "SELECT id, username, password_hash FROM users WHERE username = ?",
            (username,),
        ).fetchone()


def create_user(database_path, username, password_hash):
    with closing(sqlite3.connect(database_path)) as connection:
        connection.execute(
            "INSERT INTO users (username, password_hash) VALUES (?, ?)",
            (username, password_hash),
        )
        connection.commit()
