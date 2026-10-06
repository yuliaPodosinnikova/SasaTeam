import json
import os

DB_FILE = "data.json"

# Начальные данные по умолчанию
default_users = {
    "student": {
        "password": "123",
        "role": "student",
        "name": "Данил К.",
        "email": "student@univ.edu",
        "date": "01.12.2025"
    },
    "admin": {
        "password": "admin123",
        "role": "admin",
        "name": "Главный Администратор",
        "email": "admin@univ.edu",
        "date": "01.09.2025"
    }
}

categories_list = ["Все ❄️", "Учебники", "Электроника", "Конспекти", "Вещи", "Услуги", "Праздник"]

default_ads = [
    {
        "id": 1,
        "title": "MacBook Air M1, 2020",
        "category": "Электроника",
        "price": "62 000 ₽",
        "location": "Главный корпус",
        "time": "12 мин. назад",
        "seller_login": "student",
        "seller_name": "Данил К.",
        "rating": "4.9 ★",
        "badge": "Отличное состояние ❄️",
        "description": "Ноутбук в отличном состоянии, полный комплект. Использовался для учебы."
    },
    {
        "id": 2,
        "title": "Комплект учебников по вышмату",
        "category": "Учебники",
        "price": "1 800 ₽",
        "location": "Общежитие №3",
        "time": "35 мин. назад",
        "seller_login": "alina",
        "seller_name": "Алина М.",
        "rating": "5.0 ★",
        "badge": "Зимняя скидка",
        "description": "Учебники за 1-2 курс. Состояние хорошее, все страницы целы."
    }
]

# Текущий авторизованный пользователь в памяти
current_user = {
    "login": None,
    "data": None
}

def load_data():
    """Загрузка данных из файла JSON при запуске приложения."""
    global users_db, ads_data
    if os.path.exists(DB_FILE):
        try:
            with open(DB_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
                users_db = data.get("users", default_users)
                ads_data = data.get("ads", default_ads)
                return
        except Exception as e:
            print(f"Ошибка загрузки базы данных: {e}")
    
    users_db = default_users
    ads_data = default_ads
    save_data()

def save_data():
    """Сохранение изменений в файл JSON."""
    data = {
        "users": users_db,
        "ads": ads_data
    }
    try:
        with open(DB_FILE, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
    except Exception as e:
        print(f"Ошибка сохранения базы данных: {e}")

# Инициализация переменных базы
users_db = {}
ads_data = []
load_data()