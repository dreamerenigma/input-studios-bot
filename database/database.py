import os
import sqlite3

DB_PATH = os.path.join(os.path.dirname(__file__), 'database.db')


def create_connection():
    """Create a database connection to the SQLite database specified by db_file."""
    conn = sqlite3.connect(DB_PATH)
    return conn


def create_tables():
    """Create the necessary tables if they don't already exist."""
    conn = create_connection()
    cursor = conn.cursor()

    cursor.execute('''
       CREATE TABLE IF NOT EXISTS users (
            user_id INTEGER PRIMARY KEY AUTOINCREMENT,
            telegram_user_id INTEGER NOT NULL,
            username TEXT NOT NULL,
            is_admin BOOLEAN DEFAULT 0,
            status TEXT,
            date_added TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS telegram_messages (
            message_id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            message_text TEXT,
            message_date TIMESTAMP,
            is_deleted BOOLEAN DEFAULT 0,
            FOREIGN KEY (user_id) REFERENCES users(user_id)
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS vk_posts (
            post_id INTEGER PRIMARY KEY,
           date_added TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    conn.commit()
    conn.close()


def add_post_to_db(post_id):
    """Добавляет ID поста в базу данных."""
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO vk_posts (post_id) VALUES (?)", (post_id,))
    conn.commit()
    conn.close()


def post_exists_in_db(post_id):
    """Проверяет, существует ли пост в базе данных."""
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT 1 FROM vk_posts WHERE post_id = ?", (post_id,))
    exists = cursor.fetchone() is not None
    conn.close()
    return exists
