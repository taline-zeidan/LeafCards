import sqlite3
import bcrypt

def get_db_connection():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    return conn, cursor


def register_user(email, password):
    conn, cursor = get_db_connection()
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    
    try:
        cursor.execute('INSERT INTO Users (Email, Password) VALUES (?, ?)', (email, hashed_password))
        conn.commit()
    except sqlite3.IntegrityError:
        print("Error: That email is already used.")
    finally:
        cursor.close()
        conn.close()

def authenticate(email, password):
    conn, cursor = get_db_connection()
    cursor.execute('SELECT Password FROM Users WHERE Email = ?', (email,))
    user = cursor.fetchone()
    cursor.close()
    conn.close()
    
    if user and bcrypt.checkpw(password.encode('utf-8'), user[0]):
        return True
    else:
        return False
    
def get_username_by_email(email):
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    
    query = """SELECT username FROM users WHERE email = ?"""
    cursor.execute(query, (email,))
    result = cursor.fetchone()
    conn.close()
    
    if result:
        return result[0]
    else:
        return "No user found with that email"

def get_user_id(email):
    conn, cursor = get_db_connection()
    cursor.execute("SELECT UserID FROM Users WHERE Email = ?", (email,))
    result = cursor.fetchone()
    cursor.close()
    conn.close()
    
    if result:
        return result[0]
    else:
        return None  # No user found with that email




