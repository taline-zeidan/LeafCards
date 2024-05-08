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
    
def get_username_id(email):
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


def get_user_by_email(email):
    """
    Fetch the username (UserID) based on the email.
    """
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    query = """SELECT UserID FROM Users WHERE Email = ?"""
    cursor.execute(query, (email,))
    result = cursor.fetchone()
    conn.close()
    if result:
        return result[0]
    else:
        return "No user found with that email"

def get_leaf_sets_for_user(user_id):
    """
    Fetch all Leaf Sets for a specific User.
    """
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    query = """SELECT ls.Leaf_Set_ID, ls.FolderName, ls.Owner_Username, ls.IsPublic, ls.Label, ls.Accuracy, ls.Likes
               FROM Leaf_Sets AS ls
               JOIN UserLeafSets AS uls ON uls.LeafSetID = ls.Leaf_Set_ID
               WHERE uls.UserID = ?"""
    cursor.execute(query, (user_id,))
    result = cursor.fetchall()
    conn.close()
    return result


def get_leaf_cards_in_leaf_set(leaf_set_id):
    """
    Fetch all Leaf Cards in a specific Leaf Set.
    """
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    query = """SELECT Leaf_Card_Name, Leaf_Card_ID, FolderID, Question, Answer, Knowledge
               FROM Leaf_Cards
               WHERE FolderID = ?"""
    cursor.execute(query, (leaf_set_id,))
    result = cursor.fetchall()
    conn.close()
    return result


def get_public_leaf_sets():
    """
    Fetch all Public Leaf Sets.
    """
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    query = """SELECT Leaf_Set_ID, FolderName, Owner_Username, IsPublic, Label, Accuracy, Likes
               FROM Leaf_Sets
               WHERE IsPublic = 1"""
    cursor.execute(query)
    result = cursor.fetchall()
    conn.close()
    return result


def get_sessions_for_user(user_id):
    """
    Fetch all Sessions for a specific User.
    """
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    query = """SELECT SessionID, Token, ExpiryDateTime
               FROM Sessions
               WHERE UserID = ?"""
    cursor.execute(query, (user_id,))
    result = cursor.fetchall()
    conn.close()
    return result


def check_folder_access(user_id, folder_id):
    """
    Check if a User has access to a specific Folder.
    """
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    query = """SELECT COUNT(*) FROM FolderAccess WHERE UserID = ? AND FolderID = ?"""
    cursor.execute(query, (user_id, folder_id))
    result = cursor.fetchone()
    conn.close()
    return result[0] > 0

def delete_user(user_id):
    """
    Delete a user by user_id and automatically cascade deletes in related tables.
    """
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    query = "DELETE FROM Users WHERE UserID = ?"
    cursor.execute(query, (user_id,))
    conn.commit()
    conn.close()

def delete_leaf_set(leaf_set_id):
    """
    Delete a leaf set by leaf_set_id and automatically cascade deletes in related tables.
    """
    conn = sqlite3.connect('databas.db')
    cursor = conn.cursor()
    query = "DELETE FROM Leaf_Sets WHERE Leaf_Set_ID = ?"
    cursor.execute(query, (leaf_set_id,))
    conn.commit()
    conn.close()

