import sqlite3
import os

DB_PATH = "market.db"

def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row  # Позволяет обращаться к полям по имени (like dict)
    return conn

def init_db():
    with get_connection() as conn:
        cursor = conn.cursor()
        
        # Таблица пользователей
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                login TEXT PRIMARY KEY,
                password TEXT NOT NULL,
                name TEXT NOT NULL,
                email TEXT NOT NULL,
                role TEXT NOT NULL,
                date TEXT NOT NULL,
                avatar TEXT
            )
        """)
        
        # Таблица объявлений
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS ads (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                category TEXT NOT NULL,
                price TEXT NOT NULL,
                location TEXT NOT NULL,
                time TEXT NOT NULL,
                seller_login TEXT NOT NULL,
                seller_name TEXT NOT NULL,
                rating TEXT DEFAULT '5.0 ★',
                badge TEXT DEFAULT 'Новое ❄',
                description TEXT DEFAULT '',
                FOREIGN KEY (seller_login) REFERENCES users (login)
            )
        """)
        
        # Добавляем тестовых пользователей, если база пустая
        cursor.execute("SELECT COUNT(*) FROM users")
        if cursor.fetchone()[0] == 0:
            default_avatar = os.path.join("assets", "пончик.jpg")
            cursor.executemany("""
                INSERT INTO users (login, password, name, email, role, date, avatar)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, [
                ("admin", "1234", "Главный Админ", "admin@study.ru", "admin", "01.01.2025", default_avatar),
                ("student", "1234", "Иван Иванов", "student@study.ru", "student", "15.01.2025", default_avatar)
            ])
            
            # Добавляем стартовые объявления
            cursor.executemany("""
                INSERT INTO ads (title, category, price, location, time, seller_login, seller_name, rating, badge, description)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, [
                ("Конспекты по высшей математике", "Учеба 📚", "300 ₽", "Корпус А", "10 минут назад", "student", "Иван Иванов", "5.0 ★", "Хит ❄", "Полный курс за 1 семестр с решениями."),
                ("Ноутбук для учебы", "Электроника 💻", "15000 ₽", "Общежитие №2", "1 час назад", "admin", "Главный Админ", "4.9 ★", "Торг", "В хорошем состоянии, подходит для написания кода.")
            ])
        conn.commit()

categories_list = ["Все ❄️", "Учеба 📚", "Электроника 💻", "Одежда 👕", "Услуги 🛠", "Разное 🎁"]

current_user = None  # Глобальное хранение авторизованного юзера

# Функции-хелперы для работы с БД

def authenticate(login, password):
    global current_user
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE login = ? AND password = ?", (login, password))
        row = cursor.fetchone()
        if row:
            user_dict = dict(row)
            current_user = {
                "login": user_dict["login"],
                "data": user_dict
            }
            return True
    return False

def register_user(login, password, name, email, role="student"):
    default_avatar = os.path.join("assets", "пончик.jpg")
    try:
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO users (login, password, name, email, role, date, avatar)
                VALUES (?, ?, ?, ?, ?, '01.02.2025', ?)
            """, (login, password, name, email, role, default_avatar))
            conn.commit()
            return True
    except sqlite3.IntegrityError:
        return False  # Логин уже занят

def get_all_ads():
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM ads ORDER BY id DESC")
        return [dict(row) for row in cursor.fetchall()]

def add_ad(title, category, price, location, seller_login, seller_name, description=""):
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO ads (title, category, price, location, time, seller_login, seller_name, description)
            VALUES (?, ?, ?, ?, 'Только что', ?, ?, ?)
        """, (title, category, price, location, seller_login, seller_name, description))
        conn.commit()

def update_ad(ad_id, title, category, price, location):
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE ads 
            SET title = ?, category = ?, price = ?, location = ?
            WHERE id = ?
        """, (title, category, price, location, ad_id))
        conn.commit()

def delete_ad(ad_id):
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM ads WHERE id = ?", (ad_id,))
        conn.commit()

# Инициализируем базу при импорте модуля
init_db()