import sqlite3

with open("database.sql", "r", encoding="utf-8") as f:
    sql_script = f.read()

conn = sqlite3.connect("database.db")
cursor = conn.cursor()
cursor.executescript(sql_script)
conn.commit()
conn.close()

print("✅ Database created and menu items loaded.")
