import sqlite3

# Connect to SQLite database (creates if not exists)
conn = sqlite3.connect("database/database.db")
cursor = conn.cursor()

# Create a sample table
cursor.execute('''
CREATE TABLE IF NOT EXISTS employees (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    department TEXT NOT NULL,
    salary INTEGER NOT NULL
)
''')

# Insert some sample data
cursor.executemany('''
INSERT INTO employees (name, department, salary) VALUES (?, ?, ?)
''', [
    ("Alice", "HR", 55000),
    ("Bob", "Engineering", 75000),
    ("Charlie", "Marketing", 60000),
    ("David", "Finance", 65000)
])

# Commit and close connection
conn.commit()
conn.close()

print("Database setup completed!")
