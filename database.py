import sqlite3

conn = sqlite3.connect('database.db')
cursor = conn.cursor()

# Create Users table with constraints specified at the time of table creation
cursor.execute('''CREATE TABLE IF NOT EXISTS Users (
    UserID INT PRIMARY KEY,
    Email VARCHAR(100) NOT NULL,
    Password VARCHAR(100) NOT NULL CHECK (LENGTH(Password) >= 5));''')

# Create Folders table with foreign key constraints specified at creation
cursor.execute('''CREATE TABLE IF NOT EXISTS Folders (
    FolderID INT PRIMARY KEY,
    UserID INT,
    FolderName VARCHAR(100),
    IsPublic BOOLEAN,
    FOREIGN KEY (UserID) REFERENCES Users(UserID));''')

# Create Flashcards table with foreign key constraints specified at creation
cursor.execute('''CREATE TABLE IF NOT EXISTS Flashcards (
    FlashcardID INT PRIMARY KEY,
    FolderID INT,
    Question TEXT,
    Answer TEXT,
    FOREIGN KEY (FolderID) REFERENCES Folders(FolderID) ON DELETE CASCADE);''')

# Create FolderAccess table with foreign key constraints specified at creation
cursor.execute('''CREATE TABLE IF NOT EXISTS FolderAccess (
    UserID INT,
    FolderID INT,
    PRIMARY KEY (UserID, FolderID),
    FOREIGN KEY (UserID) REFERENCES Users(UserID) ON DELETE CASCADE,
    FOREIGN KEY (FolderID) REFERENCES Folders(FolderID) ON DELETE CASCADE);''')

# Create Sessions table with foreign key constraints specified at creation
cursor.execute('''CREATE TABLE IF NOT EXISTS Sessions (
    SessionID INT PRIMARY KEY,
    UserID INT,
    Token VARCHAR(255),
    ExpiryDateTime DATETIME,
    FOREIGN KEY (UserID) REFERENCES Users(UserID) ON DELETE CASCADE);''')

# Commit changes to the database and close the connections
conn.commit()
cursor.close()
conn.close()
