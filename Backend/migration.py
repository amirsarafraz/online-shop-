import shutil
import os
import sqlite3

# Specify the path where the SQLite database file will be created
database_path = 'C:/Users/DATiS/Desktop/Project/Online-Shop/sorce/Database.db'

# Check if the path to the database file exists, if not create the directories
os.makedirs(os.path.dirname(database_path), exist_ok=True)

# Connect to the database
conn = sqlite3.connect(database_path)

# Create a cursor object
cur = conn.cursor()

# Create the customers table
cur.execute('''
    CREATE TABLE IF NOT EXISTS customers (
        id INTEGER PRIMARY KEY,
        name TEXT NOT NULL,
        email TEXT NOT NULL UNIQUE,
        phone TEXT NOT NULL UNIQUE
    )
            
''')
cur.execute('''
    CREATE TABLE IF NOT EXISTS products (
        id INTEGER PRIMARY KEY,
        name TEXT NOT NULL,
        email TEXT NOT NULL UNIQUE,
        phone TEXT NOT NULL UNIQUE
    )

''')

# Commit the changes and close the connection
conn.commit()
conn.close()