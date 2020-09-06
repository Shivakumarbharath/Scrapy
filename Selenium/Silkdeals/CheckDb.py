import sqlite3

db = sqlite3.connect('computers.db')
c = db.cursor()
dt = c.execute("SELECT OID,* FROM computers").fetchall()

for e in dt:
    print(e)
