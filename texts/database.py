import sqlite3


conn = sqlite3.connect('files/users.db')
cur = conn.cursor()
cur.execute("CREATE TABLE IF NOT EXISTS users(id INT); ")
cur.execute("CREATE TABLE IF NOT EXISTS block(id INT); ")


def add(id):
    if (id,) in get_id(): return
    cur.execute(f"INSERT INTO users VALUES({id});")
    conn.commit()

def get_all():
    s = cur.execute("SELECT * FROM users;").fetchall()
    conn.commit()
    return s

def count():
    s = cur.execute("SELECT COUNT(*) FROM users;").fetchone()
    conn.commit()
    return s[0]

def get_id():
    s = cur.execute("SELECT id FROM users;").fetchall()
    conn.commit()
    return s

def check_block(id):
    s = cur.execute("SELECT * FROM block; ").fetchall()
    conn.commit()
    return (id,) in s

def block(id):
    cur.execute(f"INSERT INTO block VALUES({id}); ").fetchall()
    conn.commit()

def delete(id):
    cur.execute(f"DELETE FROM block WHERE id = {id}; ").fetchall()
    conn.commit()
