import sqlite3





async def connect_db():
    global db, cr
    db = sqlite3.connect("database.db")
    cr = db.cursor()
    cr.execute('''CREATE TABLE IF NOT EXISTS users(
               id INTEGER PRIMARY KEY AUTOINCREMENT,
               name TEXT NOT NULL, 
               age INTEGER NOT NULL,
               phone TEXT NOT NULL,
               email TEXT NOT NULL,
               photo TEXT NOT NULL
    )''')
    

    db.commit()



async def create_user(name,age,phone,email,photo):
    cr.execute("INSERT INTO users(name,age,phone,email,photo)VALUES(?,?,?,?,?)",(name,age,phone,email,photo))
    db.commit()



def get_all_users():
    users = cr.execute("SELECT * FROM users").fetchall()
    return users
