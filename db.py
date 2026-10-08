import sqlite3
from datetime import datetime

DB_NAME = "database.db"

def init_db():
    """Создание таблиц БД и демо-данных при первом запуске."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    # Таблица пользователей
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            login TEXT PRIMARY KEY,
            password TEXT NOT NULL,
            name TEXT NOT NULL,
            email TEXT NOT NULL,
            role TEXT NOT NULL,
            date TEXT NOT NULL
        )
    """)

    # Таблица категорий
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS categories (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT UNIQUE NOT NULL
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
            seller_login TEXT NOT NULL,
            seller_name TEXT NOT NULL,
            rating TEXT NOT NULL,
            time TEXT NOT NULL,
            status TEXT NOT NULL,
            badge TEXT,
            description TEXT
        )
    """)

    # Таблица избранного
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS favorites (
            user_login TEXT NOT NULL,
            ad_id INTEGER NOT NULL,
            PRIMARY KEY (user_login, ad_id)
        )
    """)

    # Таблица жалоб
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS reports (
            report_id INTEGER PRIMARY KEY AUTOINCREMENT,
            ad_id INTEGER NOT NULL,
            reporter_login TEXT NOT NULL,
            reason TEXT NOT NULL,
            date TEXT NOT NULL
        )
    """)

    # Таблица отзывов
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS reviews (
            review_id INTEGER PRIMARY KEY AUTOINCREMENT,
            seller_login TEXT NOT NULL,
            reviewer_login TEXT NOT NULL,
            reviewer_name TEXT NOT NULL,
            rating INTEGER NOT NULL,
            comment TEXT NOT NULL,
            date TEXT NOT NULL
        )
    """)

    # Таблица личных сообщений
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS messages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            sender_login TEXT NOT NULL,
            receiver_login TEXT NOT NULL,
            ad_id INTEGER NOT NULL,
            text TEXT NOT NULL,
            date TEXT NOT NULL
        )
    """)

    # Базовые категории
    cursor.execute("SELECT COUNT(*) FROM categories")
    if cursor.fetchone()[0] == 0:
        default_cats = [("📚 Учеба",), ("💻 Техника",), ("🏠 Для дома",), ("👕 Одежда",), ("🎉 Досуг",)]
        cursor.executemany("INSERT INTO categories (name) VALUES (?)", default_cats)

    # Заполнение стартовыми данными
    cursor.execute("SELECT COUNT(*) FROM users")
    if cursor.fetchone()[0] == 0:
        cursor.execute("INSERT INTO users VALUES (?, ?, ?, ?, ?, ?)",
                       ("admin", "admin", "Главный Дед Мороз", "santa@study.ru", "admin", "2024-12-01"))
        cursor.execute("INSERT INTO users VALUES (?, ?, ?, ?, ?, ?)",
                       ("student", "123", "Иван Иванов", "student@study.ru", "student", "2024-12-05"))

        initial_ads = [
            ("Учебник по Высшей Математике", "📚 Учеба", "450 ₽", "Корпус А, 3 этаж", "student", "Иван Иванов", "4.9 ★", "10 мин назад", "Активно", "TOP ❄️", "Отличное состояние, все страницы на месте."),
            ("Игровая мышь Logitech G102", "💻 Техника", "1 200 ₽", "Общежитие №2", "admin", "Главный Дед Мороз", "5.0 ★", "2 часа назад", "Активно", "NEW ❄️", "Полностью рабочая, подсветка RGB."),
            ("Теплый худи САСАТИМ", "👕 Одежда", "1 800 ₽", "Главный холл", "student", "Иван Иванов", "4.8 ★", "Вчера", "Активно", "", "Размер L, очень мягкий и теплый.")
        ]
        cursor.executemany("""
            INSERT INTO ads (title, category, price, location, seller_login, seller_name, rating, time, status, badge, description)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, initial_ads)

        cursor.execute("INSERT INTO reviews (seller_login, reviewer_login, reviewer_name, rating, comment, date) VALUES (?, ?, ?, ?, ?, ?)",
                       ("student", "admin", "Главный Дед Мороз", 5, "Быстро договорились, книга в супер состоянии!", "2024-12-06 12:00"))

    conn.commit()
    conn.close()

init_db()

current_user = {
    "login": None,
    "data": None
}

# === Категории ===

def get_categories():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM categories ORDER BY id ASC")
    rows = cursor.fetchall()
    conn.close()
    return ["Все ❄️"] + [row[0] for row in rows]

def add_category(name):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO categories (name) VALUES (?)", (name,))
        conn.commit()
        conn.close()
        return True
    except sqlite3.IntegrityError:
        conn.close()
        return False

def delete_category(name):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM categories WHERE name = ?", (name,))
    conn.commit()
    conn.close()

# === Аутентификация ===

def authenticate(login, password):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT login, password, name, email, role, date FROM users WHERE login = ? AND password = ?", (login, password))
    row = cursor.fetchone()
    conn.close()

    if row:
        current_user["login"] = row[0]
        current_user["data"] = {
            "password": row[1],
            "name": row[2],
            "email": row[3],
            "role": row[4],
            "date": row[5]
        }
        return True
    return False

def register_user(login, password, name, email, role="student"):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    try:
        date_str = datetime.now().strftime("%Y-%m-%d")
        cursor.execute("INSERT INTO users VALUES (?, ?, ?, ?, ?, ?)", (login, password, name, email, role, date_str))
        conn.commit()
        conn.close()
        return True
    except sqlite3.IntegrityError:
        conn.close()
        return False

# === Объявления ===

def get_all_ads():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM ads ORDER BY id DESC")
    rows = cursor.fetchall()
    conn.close()
    
    ads = [dict(row) for row in rows]
    for ad in ads:
        rating_val, count = get_seller_rating(ad["seller_login"])
        if count > 0:
            ad["rating"] = f"{rating_val:.1f} ★ ({count})"
        else:
            ad["rating"] = "Нет оценок"
    return ads

def get_ad_by_id(ad_id):
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM ads WHERE id = ?", (ad_id,))
    row = cursor.fetchone()
    conn.close()
    return dict(row) if row else None

def add_ad(title, category, price, location, seller_login, seller_name, description=""):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO ads (title, category, price, location, seller_login, seller_name, rating, time, status, badge, description)
        VALUES (?, ?, ?, ?, ?, ?, '5.0 ★', 'Только что', 'Активно', 'NEW ❄️', ?)
    """, (title, category, price, location, seller_login, seller_name, description))
    conn.commit()
    conn.close()

def update_ad(ad_id, title, category, price, location):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("UPDATE ads SET title = ?, category = ?, price = ?, location = ? WHERE id = ?", (title, category, price, location, ad_id))
    conn.commit()
    conn.close()

def update_ad_status(ad_id, status):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("UPDATE ads SET status = ? WHERE id = ?", (status, ad_id))
    conn.commit()
    conn.close()

def delete_ad(ad_id):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM ads WHERE id = ?", (ad_id,))
    cursor.execute("DELETE FROM favorites WHERE ad_id = ?", (ad_id,))
    cursor.execute("DELETE FROM reports WHERE ad_id = ?", (ad_id,))
    cursor.execute("DELETE FROM messages WHERE ad_id = ?", (ad_id,))
    conn.commit()
    conn.close()

# === Избранное ===

def is_favorite(ad_id):
    if not current_user["login"]:
        return False
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT 1 FROM favorites WHERE user_login = ? AND ad_id = ?", (current_user["login"], ad_id))
    result = cursor.fetchone()
    conn.close()
    return result is not None

def toggle_favorite(ad_id):
    if not current_user["login"]:
        return False
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    
    if is_favorite(ad_id):
        cursor.execute("DELETE FROM favorites WHERE user_login = ? AND ad_id = ?", (current_user["login"], ad_id))
        is_fav = False
    else:
        cursor.execute("INSERT INTO favorites VALUES (?, ?)", (current_user["login"], ad_id))
        is_fav = True
        
    conn.commit()
    conn.close()
    return is_fav

def get_user_favorites():
    if not current_user["login"]:
        return []
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute("""
        SELECT a.* FROM ads a
        JOIN favorites f ON a.id = f.ad_id
        WHERE f.user_login = ?
        ORDER BY a.id DESC
    """, (current_user["login"],))
    rows = cursor.fetchall()
    conn.close()
    
    ads = [dict(row) for row in rows]
    for ad in ads:
        rating_val, count = get_seller_rating(ad["seller_login"])
        if count > 0:
            ad["rating"] = f"{rating_val:.1f} ★ ({count})"
        else:
            ad["rating"] = "Нет оценок"
    return ads

# === Жалобы ===

def add_report(ad_id, reporter_login, reason):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    date_str = datetime.now().strftime("%Y-%m-%d %H:%M")
    cursor.execute("INSERT INTO reports (ad_id, reporter_login, reason, date) VALUES (?, ?, ?, ?)",
                   (ad_id, reporter_login, reason, date_str))
    conn.commit()
    conn.close()

def get_all_reports():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute("""
        SELECT r.report_id, r.ad_id, r.reporter_login, r.reason, r.date, COALESCE(a.title, 'Удалено') as ad_title
        FROM reports r
        LEFT JOIN ads a ON r.ad_id = a.id
    """)
    rows = cursor.fetchall()
    conn.close()
    return [dict(row) for row in rows]

def delete_report(report_id):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM reports WHERE report_id = ?", (report_id,))
    conn.commit()
    conn.close()

# === Отзывы ===

def add_review(seller_login, reviewer_login, reviewer_name, rating, comment):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    date_str = datetime.now().strftime("%Y-%m-%d %H:%M")
    cursor.execute("""
        INSERT INTO reviews (seller_login, reviewer_login, reviewer_name, rating, comment, date)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (seller_login, reviewer_login, reviewer_name, rating, comment, date_str))
    conn.commit()
    conn.close()

def get_seller_reviews(seller_login):
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM reviews WHERE seller_login = ? ORDER BY review_id DESC", (seller_login,))
    rows = cursor.fetchall()
    conn.close()
    return [dict(row) for row in rows]

def get_seller_rating(seller_login):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT AVG(rating), COUNT(*) FROM reviews WHERE seller_login = ?", (seller_login,))
    row = cursor.fetchone()
    conn.close()
    
    avg_rating = row[0] if row[0] is not None else 0.0
    count = row[1]
    return avg_rating, count

# === Сообщения и Диалоги ===

def send_message(sender_login, receiver_login, ad_id, text):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    date_str = datetime.now().strftime("%Y-%m-%d %H:%M")
    cursor.execute("""
        INSERT INTO messages (sender_login, receiver_login, ad_id, text, date)
        VALUES (?, ?, ?, ?, ?)
    """, (sender_login, receiver_login, ad_id, text, date_str))
    conn.commit()
    conn.close()

def get_chat_messages(user1, user2, ad_id):
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute("""
        SELECT * FROM messages 
        WHERE ad_id = ? AND ((sender_login = ? AND receiver_login = ?) OR (sender_login = ? AND receiver_login = ?))
        ORDER BY id ASC
    """, (ad_id, user1, user2, user2, user1))
    rows = cursor.fetchall()
    conn.close()
    return [dict(row) for row in rows]

def get_user_chats(user_login):
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute("""
        SELECT m.*, 
               u1.name as sender_name, 
               u2.name as receiver_name,
               COALESCE(a.title, 'Товар удален') as ad_title,
               COALESCE(a.price, '') as ad_price
        FROM messages m
        LEFT JOIN users u1 ON m.sender_login = u1.login
        LEFT JOIN users u2 ON m.receiver_login = u2.login
        LEFT JOIN ads a ON m.ad_id = a.id
        WHERE m.sender_login = ? OR m.receiver_login = ?
        ORDER BY m.id DESC
    """, (user_login, user_login))
    rows = cursor.fetchall()
    conn.close()

    chats_dict = {}
    for r in rows:
        m = dict(r)
        other_user = m["receiver_login"] if m["sender_login"] == user_login else m["sender_login"]
        chat_key = (other_user, m["ad_id"])
        
        if chat_key not in chats_dict:
            other_name = m["receiver_name"] if m["sender_login"] == user_login else m["sender_name"]
            chats_dict[chat_key] = {
                "other_login": other_user,
                "other_name": other_name or other_user,
                "ad_id": m["ad_id"],
                "ad_title": m["ad_title"],
                "ad_price": m["ad_price"],
                "last_message": m["text"],
                "last_date": m["date"]
            }

    return list(chats_dict.values())

# === Управление пользователями и Статистика (Админ) ===

def get_all_users():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute("SELECT login, name, email, role, date FROM users ORDER BY date DESC")
    rows = cursor.fetchall()
    conn.close()
    return [dict(row) for row in rows]

def update_user_role(login, new_role):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("UPDATE users SET role = ? WHERE login = ?", (new_role, login))
    conn.commit()
    conn.close()

def delete_user(login):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM users WHERE login = ?", (login,))
    cursor.execute("DELETE FROM ads WHERE seller_login = ?", (login,))
    cursor.execute("DELETE FROM favorites WHERE user_login = ?", (login,))
    cursor.execute("DELETE FROM reports WHERE reporter_login = ?", (login,))
    cursor.execute("DELETE FROM reviews WHERE seller_login = ? OR reviewer_login = ?", (login, login))
    cursor.execute("DELETE FROM messages WHERE sender_login = ? OR receiver_login = ?", (login, login))
    conn.commit()
    conn.close()

def get_app_stats():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    
    cursor.execute("SELECT COUNT(*) FROM users")
    total_users = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM users WHERE role = 'student'")
    students_count = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM users WHERE role = 'admin'")
    admins_count = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM ads")
    total_ads = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM ads WHERE status = 'Активно'")
    active_ads = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM ads WHERE status = 'Продано'")
    sold_ads = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM categories")
    total_cats = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM reports")
    total_reports = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM reviews")
    total_reviews = cursor.fetchone()[0]

    conn.close()

    return {
        "users": total_users,
        "students": students_count,
        "admins": admins_count,
        "ads": total_ads,
        "active_ads": active_ads,
        "sold_ads": sold_ads,
        "categories": total_cats,
        "reports": total_reports,
        "reviews": total_reviews
    }