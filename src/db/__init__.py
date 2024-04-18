from .db import connection

connection.execute("""
  CREATE TABLE IF NOT EXISTS book (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    status TEXT NOT NULL DEFAULT 'processing'
  );
""")
