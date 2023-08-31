import sqlite3

from helpers.hashing import *


def connectDB():
    return sqlite3.connect("db/database.db")


def init_db():
    connection = connectDB()

    users_table = """
                CREATE TABLE IF NOT EXISTS Users (
                id INTEGER PRIMARY KEY AUTOINCREMENT ,
                username VARCHAR(50) NOT NULL,
                email VARCHAR(100) NOT NULL,
                password VARCHAR(100) NOT NULL
        )"""

    notes_table = """
        CREATE TABLE IF NOT EXISTS Notes (
        note_id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        title VARCHAR(255) NOT NULL,
        content TEXT NOT NULL,
        image_url TEXT,
        FOREIGN KEY (user_id) REFERENCES Users(id)
        );
    """

    cursor = connection.cursor()

    # creating tables execution
    cursor.execute(users_table)
    cursor.execute(notes_table)

    connection.commit()


def add_user(username, password, email):
    connection = connectDB()

    # Solved SQL-Injection
    addingQuery = f"""
        INSERT INTO users(username, password, email) VALUES(?, ?, ?)
        """

    cursor = connection.cursor()

    cursor.execute(addingQuery, (username, hash_password(password), email))

    connection.commit()


def get_user_by_username(username):
    connection = connectDB()

    gettingQuery = f"""
        SELECT * FROM users WHERE username = ?
        """

    cursor = connection.cursor()

    cursor.execute(gettingQuery, (username,))

    return cursor.fetchone()
