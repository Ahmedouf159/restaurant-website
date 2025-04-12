import sqlite3

DB_NAME = 'C:/Users/Tweety/OneDrive/Desktop/Ahmed/websites/Ahmed website 3 foods data base 1/database.db'

conn = sqlite3.connect(DB_NAME)
cursor = conn.cursor()

# Add the column 'location' if it does not exist
try:
    cursor.execute("ALTER TABLE users ADD COLUMN location TEXT;")
    conn.commit()
except sqlite3.OperationalError:
    print("Column 'location' already exists.")

conn.close()
