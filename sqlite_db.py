import sqlite3

# Create or connect to a database
conn = sqlite3.connect('example.db')

# Create a cursor object
cursor = conn.cursor()

# Create a users table in the database
# SQLite supports the following types: NULL, INTEGER, REAL, TEXT, BLOB
# cursor.execute('''CREATE TABLE users (id INTEGER PRIMARY KEY, name TEXT)''')
# conn.commit()

# Insert data into the users table
# cursor.execute("INSERT INTO users (name) VALUES ('Eneo')")
# conn.commit()

# Update data in the users table
# cursor.execute("UPDATE users SET name = 'Jane' WHERE id = 3")
# conn.commit()

# Select all data from the users table
# cursor.execute("SELECT id, name FROM users")
# print(cursor.fetchall())

# Select data from the users table where the name is Jane
# cursor.execute("SELECT * FROM users WHERE name = 'Jane'")
# print(cursor.fetchall())

# Delete data from the users table
cursor.execute("DELETE FROM users WHERE name = 'Jane'")
conn.commit()

# Close the connection
conn.close()