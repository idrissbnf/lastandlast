import mysql.connector
from mysql.connector import Error
import streamlit as st
import os

# Database configuration using environment variables with Railway.app connection details as defaults
DB_CONFIG = {
    "host": os.environ.get("DB_HOST", "mysql.railway.internal"),
    "user": os.environ.get("DB_USER", "root"),
    "password": os.environ.get("DB_PASSWORD", "HRIhlJRnFbbNnBubIVhnLPuwDuNPrMZJ"),
    "database": os.environ.get("DB_NAME", "railway"),
    "port": os.environ.get("DB_PORT", "3306")
}

def get_db_connection():
    """
    Create and return a connection to the MySQL database.
    Returns the connection object or None if connection fails.
    """
    try:
        connection = mysql.connector.connect(**DB_CONFIG)
        if connection.is_connected():
            return connection
    except Error as e:
        st.error(f"Error connecting to MySQL database: {e}")
    return None

def init_database():
    """
    Initialize the database by creating tables if they don't exist.
    """
    try:
        connection = get_db_connection()
        if connection is None:
            st.error("Failed to connect to the database for initialization.")
            return False
        
        cursor = connection.cursor()
        
        # Create users table if it doesn't exist
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INT AUTO_INCREMENT PRIMARY KEY,
            username VARCHAR(50) UNIQUE NOT NULL,
            password VARCHAR(255) NOT NULL,
            email VARCHAR(100),
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """)
        
        connection.commit()
        cursor.close()
        connection.close()
        return True
    except Error as e:
        st.error(f"Error initializing database: {e}")
        return False

def authenticate_user(username, password):
    """
    Authenticate a user with username and password against MySQL database.
    Returns True if authentication is successful, False otherwise.
    """
    try:
        connection = get_db_connection()
        if connection is None:
            return False
        
        cursor = connection.cursor(dictionary=True)
        
        # Check if username and password match
        query = "SELECT * FROM users WHERE username = %s AND password = %s"
        cursor.execute(query, (username, password))
        
        result = cursor.fetchone()
        
        cursor.close()
        connection.close()
        
        return result is not None
    except Error as e:
        st.error(f"Error during authentication: {e}")
        return False

def register_user(username, password, email=""):
    """
    Register a new user in the MySQL database.
    Returns:
    - "success" if registration successful
    - "exists" if username already exists
    - "error" on other errors
    """
    try:
        connection = get_db_connection()
        if connection is None:
            return "error"
        
        cursor = connection.cursor(dictionary=True)
        
        # Check if username already exists
        check_query = "SELECT * FROM users WHERE username = %s"
        cursor.execute(check_query, (username,))
        if cursor.fetchone() is not None:
            cursor.close()
            connection.close()
            return "exists"
        
        # Insert new user
        insert_query = "INSERT INTO users (username, password, email) VALUES (%s, %s, %s)"
        cursor.execute(insert_query, (username, password, email))
        
        connection.commit()
        cursor.close()
        connection.close()
        return "success"
    except Error as e:
        st.error(f"Error registering user: {e}")
        return "error"

def get_user_info(username):
    """
    Get user information from the database.
    Returns user data as a dictionary or None if user doesn't exist.
    """
    try:
        connection = get_db_connection()
        if connection is None:
            return None
        
        cursor = connection.cursor(dictionary=True)
        
        query = "SELECT id, username, email, created_at FROM users WHERE username = %s"
        cursor.execute(query, (username,))
        
        user = cursor.fetchone()
        
        cursor.close()
        connection.close()
        
        return user
    except Error as e:
        st.error(f"Error retrieving user info: {e}")
        return None