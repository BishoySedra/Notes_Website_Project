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
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        title VARCHAR(255) NOT NULL,
        content TEXT NOT NULL,
        image_url TEXT DEFAULT NULL,
        FOREIGN KEY (user_id) REFERENCES Users(id)
        );
    """
    plans_table = """
        CREATE TABLE IF NOT EXISTS plans (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title VARCHAR(255) NOT NULL,
        price DECIMAL(10, 2) NOT NULL,
        description TEXT NOT NULL
        );
    """

    users_plans_table = """
        CREATE TABLE IF NOT EXISTS UserPlans (
        user_plan_id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        plan_id INTEGER,
        PurchaseDate TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (user_id) REFERENCES Users(id),
        FOREIGN KEY (plan_id) REFERENCES Plans(id)
        );
    """

    cursor = connection.cursor()

    # creating tables execution
    cursor.execute(users_table)
    cursor.execute(notes_table)
    cursor.execute(plans_table)
    cursor.execute(users_plans_table)

    # save changes on database
    connection.commit()


def create_admin():
    connection = connectDB()

    if not get_user_by_username("admin"):
        # create admin user
        admin_creation = """
            INSERT INTO users(username, password, email) VALUES(?, ?, ?)
        """

        cursor = connection.cursor()

        cursor.execute(
            admin_creation, ("admin", hash_password("Admin@123"), "admin@gmail.com")
        )

        connection.commit()
    else:
        print("Admin already existed!")


def get_plan_by_id(plan_id):
    connection = connectDB()
    query = """
    SELECT * FROM plans where id = ?
    """
    cursor = connection.cursor()
    cursor.execute(query, (plan_id))
    return cursor.fetchone()


def add_purchase(user_id, plan_id):
    connection = connectDB()
    query = """
        INSERT INTO UserPlans(user_id,plan_id) VALUES(?, ?)
        """
    cursor = connection.cursor()
    cursor.execute(query, (user_id, plan_id))
    connection.commit()


def get_purchases(plan_id,user_id):
    connection = connectDB()
    query = """
            select user_id ,plan_id from UserPlans where plan_id = ? AND user_id=?
            """
    cursor = connection.cursor()
    cursor.execute(query, (plan_id,user_id))
    connection.commit()
    return cursor.fetchall()

def get_purchases_by_user_id(user_id):
    connection = connectDB()
    query = """
            select plan_id from UserPlans where user_id = ?
            """
    cursor = connection.cursor()
    cursor.execute(query, (user_id,))
    connection.commit()
    return cursor.fetchall()

def get_all_plans():
    connection = connectDB()
    query = """
    SELECT * FROM plans
    """
    cursor = connection.cursor()
    cursor.execute(query)
    connection.commit()
    return cursor.fetchall()
    


def add_plan(title, price, description):
    connection = connectDB()

    # Solved SQL-Injection
    addingQuery = f"""
        INSERT INTO plans(title, price, description) VALUES(?, ?, ?)
        """

    cursor = connection.cursor()

    cursor.execute(addingQuery, (title, price, description))

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


def add_note(user_id, category, content, image=""):
    connection = connectDB()
    query = """
    INSERT INTO notes (user_id,title,content,image_url) VALUES (?,?,?,?) 
    """
    cursor = connection.cursor()
    cursor.execute(query, (user_id, category, content, image))

    connection.commit()


def get_all_notes(user_id):
    connection = connectDB()
    query = """
    SELECT * FROM NOTES WHERE user_id = ?
    """
    cursor = connection.cursor()
    cursor.execute(query, (user_id,))
    return cursor.fetchall()


def get_note_by_title(user_id, title):
    connection = connectDB()
    query = """ select * FROM NOTES WHERE (user_id=? and title=? )  """

    cursor = connection.cursor()
    cursor.execute(query, (user_id, title))
    return cursor.fetchall()
