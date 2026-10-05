import customtkinter as ctk
import random

# --- Настройки темы ---
ctk.set_appearance_mode("Light")
ctk.set_default_color_theme("blue")

class NewYearMarketApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Новогодний Маркетплейс ❄️")
        self.geometry("420x840")
        self.resizable(False, False)

        # Данные объявлений
        self.ads_data = [
            {
                "id": 1,
                "title": "MacBook Air M1, 2020",
                "category": "Электроника 💻",
                "price": "62 000 ₽",
                "location": "Главный корпус",
                "time": "12 мин. назад",
                "seller": "Данил К.",
                "rating": "4.9 ★",
                "badge": "Отличное состояние ❄️",
                "badge_color": "#E0F2FE",
                "badge_text_color": "#0369A1"
            },
            {
                "id": 2,
                "title": "Комплект учебников по вышмату",
                "category": "Учебники 📚",
                "price": "1 800 ₽",
                "location": "Общежитие №3",
                "time": "35 мин. назад",
                "seller": "Алина М.",
                "rating": "5.0 ★",
                "badge": "Зимняя скидка 🏷️",
                "badge_color": "#DBEAFE",
                "badge_text_color": "#1D4ED8"
            },
            {
                "id": 3,
                "title": "Новогодняя гирлянда и свитер",
                "category": "Праздник 🎄",
                "price": "900 ₽",
                "location": "Общежитие №1",
                "time": "1 час назад",
                "seller": "Иван В.",
                "rating": "4.8 ★",
                "badge": "Новогодний подарок 🎁",
                "badge_color": "#E0F2FE",
                "badge_text_color": "#0284C7"
            }
        ]

        # --- Основной контейнер (Светло-голубой морозный фон) ---
        self.main_container = ctk.CTkFrame(self, fg_color="#F0F9FF", corner_radius=0)
        self.main_container.pack(fill="both", expand=True)

        # --- 1. ВЕРХНЯЯ ПАНЕЛЬ (HEADER) ---
        self.header_frame = ctk.CTkFrame(self.main_container, fg_color="transparent")
        self.header_frame.pack(fill="x", padx=16, pady=(12, 6))

        # Логотип "С ❄️" и Аватар
        self.logo_avatar_row = ctk.CTkFrame(self.header_frame, fg_color="transparent")
        self.logo_avatar_row.pack(fill="x")

        self.logo_btn = ctk.CTkButton(
            self.logo_avatar_row, text="С ❄️", width=38, height=38, 
            corner_radius=12, fg_color="#0284C7", hover_color="#0369A1", 
            font=("Arial", 15, "bold")
        )
        self.logo_btn.pack(side="left")

        self.avatar_frame = ctk.CTkFrame(self.logo_avatar_row, fg_color="transparent")
        self.avatar_frame.pack(side="right")

        self.notif_btn = ctk.CTkLabel(self.avatar_frame, text="🔔", font=("Arial", 16))
        self.notif_btn.pack(side="left", padx=8)

        self.avatar = ctk.CTkButton(
            self.avatar_frame, text="АК 👤", width=38, height=38, 
            corner_radius=19, fg_color="#E0F2FE", text_color="#0369A1", 
            font=("Arial", 11, "bold")
        )
        self.avatar.pack(side="left")

        # Поле поиска
        self.search_entry = ctk.CTkEntry(
            self.header_frame, placeholder_text="🔍  Поиск по объявлениям...", 
            height=42, corner_radius=12, fg_color="#FFFFFF", border_color="#BAE6FD"
        )
        self.search_entry.pack(fill="x", pady=(10, 0))

        # --- СКОЛЬЗЯЩАЯ ОБЛАСТЬ (SCROLLABLE) ---
        self.scroll_frame = ctk.CTkScrollableFrame(self.main_container, fg_color="transparent", corner_radius=0)
        self.scroll_frame.pack(fill="both", expand=True, padx=0, pady=0)

        # --- 2. БАННЕР С СНЕГОМ И АНИМАЦИЕЙ ---
        self.banner_frame = ctk.CTkFrame(self.scroll_frame, fg_color="#0284C7", corner_radius=16)
        self.banner_frame.pack(fill="x", padx=16, pady=8)

        # Анимированный холст для снежинок
        self.snow_canvas = ctk.CTkCanvas(
            self.banner_frame, width=380, height=150, 
            bg="#0284C7", highlightthickness=0
        )
        self.snow_canvas.pack(fill="both", expand=True)

        # Текст поверх баннера
        self.snow_canvas.create_text(
            16, 20, anchor="w", text="🛡️  Только для студентов", 
            fill="#BAE6FD", font=("Arial", 10, "bold")
        )
        self.snow_canvas.create_text(
            16, 50, anchor="w", text="Всё нужное для учёбы — рядом", 
            fill="#FFFFFF", font=("Arial", 16, "bold")
        )
        self.snow_canvas.create_text(
            16, 78, anchor="w", text="Покупайте, продавайте и обменивайтесь\nвнутри университета. Безопасно и быстро.", 
            fill="#E0F2FE", font=("Arial", 10)
        )

        # Создание снежинок
        self.snowflakes = []
        for _ in range(25):
            x = random.randint(0, 380)
            y = random.randint(0, 150)
            size = random.randint(2, 5)
            speed = random.uniform(1.0, 2.5)
            flake = self.snow_canvas.create_oval(x, y, x + size, y + size, fill="#FFFFFF", outline="")
            self.snowflakes.append({"id": flake, "x": x, "y": y, "speed": speed, "size": size})

        # Кнопка подачи объявления в баннере
        self.add_ad_btn = ctk.CTkButton(
            self.banner_frame, text="+ Подать объявление", 
            fg_color="#FFFFFF", hover_color="#F1F5F9", text_color="#0284C7",
            corner_radius=10, font=("Arial", 12, "bold"), height=36
        )
        self.add_ad_btn.pack(anchor="w", padx=16, pady=(0, 14))

        # Запуск анимации снега
        self.animate_snow()

        # --- 3. КАТЕГОРИИ ---
        self.cats_frame = ctk.CTkFrame(self.scroll_frame, fg_color="transparent")
        self.cats_frame.pack(fill="x", padx=16, pady=6)

        cats = ["Все объявления ❄️", "Учебники 📚", "Электроника 💻", "Праздник 🎄"]
        for i, cat in enumerate(cats):
            is_active = (i == 0)
            btn = ctk.CTkButton(
                self.cats_frame, text=cat, height=32, corner_radius=10,
                fg_color="#0284C7" if is_active else "#FFFFFF",
                text_color="#FFFFFF" if is_active else "#0F172A",
                border_width=1 if not is_active else 0, border_color="#BAE6FD",
                font=("Arial", 11)
            )
            btn.pack(side="left", padx=(0, 6))

        # Заголовок ленты
        self.feed_header = ctk.CTkFrame(self.scroll_frame, fg_color="transparent")
        self.feed_header.pack(fill="x", padx=16, pady=(10, 4))

        ctk.CTkLabel(self.feed_header, text="Свежие предложения", font=("Arial", 11, "bold"), text_color="#0284C7").pack(anchor="w")
        ctk.CTkLabel(self.feed_header, text="Все объявления", font=("Arial", 16, "bold"), text_color="#0F172A").pack(anchor="w")

        # --- 4. ЛЕНТА ОБЪЯВЛЕНИЙ ---
        self.feed_container = ctk.CTkFrame(self.scroll_frame, fg_color="transparent")
        self.feed_container.pack(fill="x", padx=16, pady=4)

        self.render_feed()

        # --- 5. НИЖНЯЯ НАВИГАЦИЯ (BOTTOM BAR) ---
        self.bottom_bar = ctk.CTkFrame(self.main_container, fg_color="#FFFFFF", height=60, corner_radius=0, border_width=1, border_color="#E0F2FE")
        self.bottom_bar.pack(fill="x", side="bottom")

        nav_items = ["🏠", "❤️", "➕", "💬", "👤"]
        for item in nav_items:
            if item == "➕":
                btn = ctk.CTkButton(self.bottom_bar, text=item, width=44, height=44, corner_radius=22, fg_color="#0284C7", hover_color="#0369A1", font=("Arial", 18))
            else:
                btn = ctk.CTkButton(self.bottom_bar, text=item, width=40, height=40, fg_color="transparent", text_color="#64748B", font=("Arial", 16))
            btn.pack(side="left", expand=True, pady=8)

    def animate_snow(self):
        """ Движение снежинок сверху вниз """
        for flake in self.snowflakes:
            flake["y"] += flake["speed"]
            if flake["y"] > 150:
                flake["y"] = -5
                flake["x"] = random.randint(0, 380)
            self.snow_canvas.coords(flake["id"], flake["x"], flake["y"], flake["x"] + flake["size"], flake["y"] + flake["size"])
        
        self.after(50, self.animate_snow)

    def render_feed(self):
        for ad in self.ads_data:
            # Карточка
            card = ctk.CTkFrame(self.feed_container, fg_color="#FFFFFF", corner_radius=16, border_width=1, border_color="#E0F2FE")
            card.pack(fill="x", pady=8)

            # Картинка-заглушка
            img_placeholder = ctk.CTkFrame(card, fg_color="#38BDF8", height=120, corner_radius=12)
            img_placeholder.pack(fill="x", padx=8, pady=8)

            # Новогодний бейдж
            badge = ctk.CTkLabel(
                img_placeholder, text=ad["badge"], 
                fg_color=ad["badge_color"], text_color=ad["badge_text_color"], 
                corner_radius=6, font=("Arial", 9, "bold")
            )
            badge.pack(anchor="nw", padx=8, pady=8)

            # Инфо
            info_frame = ctk.CTkFrame(card, fg_color="transparent")
            info_frame.pack(fill="x", padx=12, pady=(0, 10))

            ctk.CTkLabel(info_frame, text=ad["category"], font=("Arial", 10, "bold"), text_color="#0284C7").pack(anchor="w")

            title_row = ctk.CTkFrame(info_frame, fg_color="transparent")
            title_row.pack(fill="x")

            ctk.CTkLabel(title_row, text=ad["title"], font=("Arial", 13, "bold"), text_color="#0F172A").pack(side="left")
            ctk.CTkLabel(title_row, text=ad["price"], font=("Arial", 14, "bold"), text_color="#0284C7").pack(side="right")

            loc_time = f"📍 {ad['location']}  •  🕒 {ad['time']}"
            ctk.CTkLabel(info_frame, text=loc_time, font=("Arial", 10), text_color="#64748B").pack(anchor="w", pady=2)

            seller_row = ctk.CTkFrame(info_frame, fg_color="transparent")
            seller_row.pack(fill="x", pady=(6, 0))

            ctk.CTkLabel(seller_row, text=f"👤 {ad['seller']}", font=("Arial", 11), text_color="#334151").pack(side="left")
            ctk.CTkLabel(seller_row, text=ad["rating"], font=("Arial", 11, "bold"), text_color="#D97706").pack(side="right")

if __name__ == "__main__":
    app = NewYearMarketApp()
    app.mainloop()