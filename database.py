# database.py

import sqlite3
from datetime import datetime

DB_PATH = "bot_database.db"

def init_db():
    """Инициализация таблицы пользователей"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            user_id INTEGER PRIMARY KEY,
            username TEXT,
            first_seen TEXT
        )
    """)
    conn.commit()
    conn.close()

def add_or_update_user(user_id: int, username: str):
    """Добавляет пользователя или обновляет его username, если он сменился"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute("SELECT user_id FROM users WHERE user_id = ?", (user_id,))
    user = cursor.fetchone()
    
    formatted_username = f"@{username}" if username else "Без username"
    
    if not user:
        today_date = datetime.now().strftime("%d.%m.%Y")
        cursor.execute(
            "INSERT INTO users (user_id, username, first_seen) VALUES (?, ?, ?)",
            (user_id, formatted_username, today_date)
        )
    else:
        cursor.execute(
            "UPDATE users SET username = ? WHERE user_id = ?",
            (formatted_username, user_id)
        )
        
    conn.commit()
    conn.close()

def get_users_count() -> int:
    """Возвращает общее количество пользователей"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM users")
    count = cursor.fetchone()[0]
    conn.close()
    return count

def get_all_user_ids() -> list:
    """Возвращает список всех ID для рассылки"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT user_id FROM users")
    users = [row[0] for row in cursor.fetchall()]
    conn.close()
    return users

def export_users_txt(filename: str = "users_list.txt"):
    """Экспортирует список пользователей с датами в txt-файл"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT username, first_seen FROM users")
    rows = cursor.fetchall()
    conn.close()
    
    with open(filename, "w", encoding="utf-8") as f:
        f.write("ЮЗЕРНЕЙМ | ДАТА ПЕРВОГО ВХОДА\n")
        f.write("=" * 35 + "\n")
        for username, first_seen in rows:
            f.write(f"{username:<20} | {first_seen}\n")
            
    return filename