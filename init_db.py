import sqlite3

# Initialize or reset the database
conn = sqlite3.connect('url_shortener.db')

# Create the `urls` table if it doesn't exist
conn.execute('''
CREATE TABLE IF NOT EXISTS urls (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    original_url TEXT NOT NULL,
    short_code TEXT NOT NULL UNIQUE,
    clicks INTEGER DEFAULT 0
)
''')

conn.commit()
conn.close()
print("Database initialized successfully.")
