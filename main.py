import customtkinter as ctk
import random
from tkinter import messagebox

# --- Настройки темы ---
ctk.set_appearance_mode("Dark")


class NewYearMarketApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Новогодний Маркетплейс ❄️")
        self.geometry("420x840")
        self.resizable(False, False)

        # Текущая роль ("student" или "admin")
        self.current_role = None

        # Цветовая палитра
        self.COLOR_BG = "#25330F"       # Основной фон (Темно-зеленый/оливковый)
        self.COLOR_ACCENT = "#741102"   # Мелкие детали и кнопки (Темно-красный)
        self.COLOR_TEXT = "#D4C9B4"     # Текст и иконки (Кремовый/бежевый)
        self.COLOR_CARD_BG = "#1D280B"  # Фон карточек и полей

        self.configure(fg_color=self.COLOR_BG)

        # Цветовая палитра лампочек с фото
        self.bulb_colors = ["#FF1E27", "#00FF66", "#007EFF", "#FFD700", "#FF007F"]
        self.garland_bulbs = []

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
                "badge": "Отличное состояние ❄️️"
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
                "badge": "Зимняя скидка 🏷️"
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
                "badge": "Новогодний подарок 🎁"
            }
        ]

        # Главный контейнер
        self.main_container = ctk.CTkFrame(self, fg_color=self.COLOR_BG, corner_radius=0)
        self.main_container.pack(fill="both", expand=True)

        # Показываем экран авторизации при запуске
        self.show_login_screen()

    # ==========================================
    # --- 1. ЭКРАН АВТОРИЗАЦИИ И ВЫБОРА РОЛИ ---
    # ==========================================
    def show_login_screen(self):
        for widget in self.main_container.winfo_children():
            widget.destroy()

        login_card = ctk.CTkFrame(
            self.main_container, 
            fg_color=self.COLOR_CARD_BG, 
            corner_radius=20, 
            border_width=1, 
            border_color=self.COLOR_ACCENT
        )
        login_card.pack(fill="both", expand=True, padx=24, pady=80)

        # Заголовок
        ctk.CTkLabel(login_card, text="❄️", font=("Arial", 40), text_color=self.COLOR_TEXT).pack(pady=(30, 5))
        ctk.CTkLabel(login_card, text="Студенческий Маркет", font=("Arial", 20, "bold"), text_color=self.COLOR_TEXT).pack()
        ctk.CTkLabel(login_card, text="Выберите роль для входа в систему", font=("Arial", 11), text_color=self.COLOR_TEXT).pack(pady=(2, 20))

        # Выбор роли (Segmented Button)
        self.role_var = ctk.StringVar(value="Студент 🎓")
        self.role_selector = ctk.CTkSegmentedButton(
            login_card,
            values=["Студент 🎓", "Администратор 🔑"],
            variable=self.role_var,
            command=self.on_role_change,
            selected_color=self.COLOR_ACCENT,
            selected_hover_color="#520B01",
            unselected_color=self.COLOR_BG,
            unselected_hover_color=self.COLOR_ACCENT,
            text_color=self.COLOR_TEXT,
            height=38
        )
        self.role_selector.pack(fill="x", padx=20, pady=10)

        # Поле ввода пароля (скрыто по умолчанию)
        self.password_frame = ctk.CTkFrame(login_card, fg_color="transparent")
        self.password_label = ctk.CTkLabel(self.password_frame, text="Пароль администратора:", font=("Arial", 11, "bold"), text_color=self.COLOR_TEXT)
        self.password_label.pack(anchor="w", pady=(0, 4))
        
        self.password_entry = ctk.CTkEntry(
            self.password_frame,
            placeholder_text="Введите пароль...",
            show="*",
            height=40,
            corner_radius=10,
            border_color=self.COLOR_ACCENT,
            fg_color=self.COLOR_BG,
            text_color=self.COLOR_TEXT,
            placeholder_text_color="#8C8373"
        )
        self.password_entry.pack(fill="x")
        
        # Подсказка
        self.hint_label = ctk.CTkLabel(login_card, text="Вход для студентов доступен без пароля", font=("Arial", 10), text_color=self.COLOR_TEXT)
        self.hint_label.pack(pady=10)

        # Кнопка Войти
        self.login_btn = ctk.CTkButton(
            login_card,
            text="Войти в маркетплейс",
            fg_color=self.COLOR_ACCENT,
            hover_color="#520B01",
            text_color=self.COLOR_TEXT,
            height=44,
            corner_radius=12,
            font=("Arial", 13, "bold"),
            command=self.handle_login
        )
        self.login_btn.pack(fill="x", padx=20, pady=(10, 20))

    def on_role_change(self, value):
        if value == "Администратор 🔑":
            self.password_frame.pack(fill="x", padx=20, pady=10)
            self.hint_label.configure(text="Пароль по умолчанию: admin123")
        else:
            self.password_frame.pack_forget()
            self.hint_label.configure(text="Вход для студентов доступен без пароля")

    def handle_login(self):
        selected_role = self.role_var.get()
        
        if selected_role == "Администратор 🔑":
            entered_password = self.password_entry.get()
            if entered_password == "admin123":
                self.current_role = "admin"
                self.build_main_interface()
            else:
                messagebox.showerror("Ошибка доступа", "Неверный пароль администратора!")
        else:
            self.current_role = "student"
            self.build_main_interface()

    # ==========================================
    # --- 2. ГЛАВНЫЙ ИНТЕРФЕЙС ПРИЛОЖЕНИЯ ---
    # ==========================================
    def build_main_interface(self):
        for widget in self.main_container.winfo_children():
            widget.destroy()

        # --- 0. РЕАЛИСТИЧНАЯ ГИРЛЯНДА С ПРОВОДАМИ И ЛАМПОЧКАМИ ---
        self.garland_canvas = ctk.CTkCanvas(
            self.main_container,
            width=420,
            height=32,
            bg=self.COLOR_CARD_BG,
            highlightthickness=0
        )
        self.garland_canvas.pack(fill="x", side="top")

        self.draw_garland()
        self.animate_garland()

        # --- 1. ВЕРХНЯЯ ПАНЕЛЬ (HEADER) И НОВОГОДНЯЯ ШАПКА ---
        self.header_frame = ctk.CTkFrame(self.main_container, fg_color="transparent")
        self.header_frame.pack(fill="x", padx=16, pady=(8, 6))

        self.logo_avatar_row = ctk.CTkFrame(self.header_frame, fg_color="transparent")
        self.logo_avatar_row.pack(fill="x")

        # Контейнер для логотипа и нарисованной новогодней шапки над ним
        self.logo_container = ctk.CTkFrame(self.logo_avatar_row, fg_color="transparent")
        self.logo_container.pack(side="left")

        # Холст для рисования новогодней шапки Санты
        self.hat_canvas = ctk.CTkCanvas(self.logo_container, width=46, height=22, bg=self.COLOR_BG, highlightthickness=0)
        self.hat_canvas.pack(side="top", anchor="w")
        self.draw_santa_hat(self.hat_canvas)

        self.logo_btn = ctk.CTkButton(
            self.logo_container, text="С ❄️", width=38, height=38, 
            corner_radius=12, fg_color=self.COLOR_ACCENT, hover_color="#520B01", 
            text_color=self.COLOR_TEXT, font=("Arial", 15, "bold")
        )
        self.logo_btn.pack(side="top")

        self.avatar_frame = ctk.CTkFrame(self.logo_avatar_row, fg_color="transparent")
        self.avatar_frame.pack(side="right", pady=(18, 0))

        role_title = "Админ 🔑" if self.current_role == "admin" else "Студент 🎓"

        self.role_badge = ctk.CTkLabel(
            self.avatar_frame, text=role_title, fg_color=self.COLOR_ACCENT, text_color=self.COLOR_TEXT,
            corner_radius=10, font=("Arial", 10, "bold"), padx=8, pady=4
        )
        self.role_badge.pack(side="left", padx=(0, 6))

        # Аватарка с новогодней шапкой 🎅
        self.avatar = ctk.CTkButton(
            self.avatar_frame, 
            text="🎅 АК", 
            width=42, 
            height=38, 
            corner_radius=19, 
            fg_color=self.COLOR_ACCENT, 
            hover_color="#520B01", 
            text_color=self.COLOR_TEXT, 
            font=("Arial", 11, "bold")
        )
        self.avatar.pack(side="left", padx=(0, 6))

        # Кнопка Выход
        self.logout_btn = ctk.CTkButton(
            self.avatar_frame, text="🚪", width=34, height=34, 
            corner_radius=17, fg_color=self.COLOR_ACCENT, hover_color="#520B01", text_color=self.COLOR_TEXT,
            font=("Arial", 13), command=self.show_login_screen
        )
        self.logout_btn.pack(side="left")

        # Поле поиска
        self.search_entry = ctk.CTkEntry(
            self.header_frame, placeholder_text="🔍  Поиск по объявлениям...", 
            height=42, corner_radius=12, fg_color=self.COLOR_CARD_BG, 
            border_color=self.COLOR_ACCENT, text_color=self.COLOR_TEXT,
            placeholder_text_color="#8C8373"
        )
        self.search_entry.pack(fill="x", pady=(10, 0))

        # --- СКОЛЬЗЯЩАЯ ОБЛАСТЬ ---
        self.scroll_frame = ctk.CTkScrollableFrame(self.main_container, fg_color="transparent", corner_radius=0)
        self.scroll_frame.pack(fill="both", expand=True, padx=0, pady=0)

        # --- 2. БАННЕР С СНЕГОМ И АНИМАЦИЕЙ ---
        self.banner_frame = ctk.CTkFrame(self.scroll_frame, fg_color=self.COLOR_CARD_BG, corner_radius=16, border_width=1, border_color=self.COLOR_ACCENT)
        self.banner_frame.pack(fill="x", padx=16, pady=8)

        self.snow_canvas = ctk.CTkCanvas(
            self.banner_frame, width=380, height=130, 
            bg=self.COLOR_CARD_BG, highlightthickness=0
        )
        self.snow_canvas.pack(fill="both", expand=True)

        banner_subtitle = "🛡️ Режим Администратора" if self.current_role == "admin" else "🛡️️ Только для студентов"
        self.snow_canvas.create_text(16, 20, anchor="w", text=banner_subtitle, fill=self.COLOR_TEXT, font=("Arial", 10, "bold"))
        self.snow_canvas.create_text(16, 46, anchor="w", text="Всё нужное для учёбы — рядом", fill=self.COLOR_TEXT, font=("Arial", 15, "bold"))
        self.snow_canvas.create_text(16, 72, anchor="w", text="Покупайте, продавайте и обменивайтесь\nвнутри университета. Безопасно и быстро.", fill=self.COLOR_TEXT, font=("Arial", 10))

        # Снежинки
        self.snowflakes = []
        for _ in range(25):
            x = random.randint(0, 380)
            y = random.randint(0, 130)
            size = random.randint(2, 5)
            speed = random.uniform(1.0, 2.5)
            flake = self.snow_canvas.create_oval(x, y, x + size, y + size, fill=self.COLOR_TEXT, outline="")
            self.snowflakes.append({"id": flake, "x": x, "y": y, "speed": speed, "size": size})

        self.add_ad_btn = ctk.CTkButton(
            self.banner_frame, text="+ Подать объявление", 
            fg_color=self.COLOR_ACCENT, hover_color="#520B01", text_color=self.COLOR_TEXT,
            corner_radius=10, font=("Arial", 12, "bold"), height=34
        )
        self.add_ad_btn.pack(anchor="w", padx=16, pady=(0, 12))

        self.animate_snow()

        # --- 3. КАТЕГОРИИ ---
        self.cats_frame = ctk.CTkFrame(self.scroll_frame, fg_color="transparent")
        self.cats_frame.pack(fill="x", padx=16, pady=6)

        cats = ["Все ❄️", "Учебники 📚", "Электроника 💻", "Праздник 🎄"]
        for i, cat in enumerate(cats):
            is_active = (i == 0)
            btn = ctk.CTkButton(
                self.cats_frame, text=cat, height=32, corner_radius=10,
                fg_color=self.COLOR_ACCENT if is_active else self.COLOR_CARD_BG,
                hover_color="#520B01" if is_active else self.COLOR_ACCENT,
                text_color=self.COLOR_TEXT,
                border_width=1, border_color=self.COLOR_ACCENT,
                font=("Arial", 11)
            )
            btn.pack(side="left", padx=(0, 6))

        # Заголовок ленты
        self.feed_header = ctk.CTkFrame(self.scroll_frame, fg_color="transparent")
        self.feed_header.pack(fill="x", padx=16, pady=(10, 4))

        ctk.CTkLabel(self.feed_header, text="Свежие предложения", font=("Arial", 11, "bold"), text_color=self.COLOR_TEXT).pack(anchor="w")
        ctk.CTkLabel(self.feed_header, text="Лента объявлений", font=("Arial", 16, "bold"), text_color=self.COLOR_TEXT).pack(anchor="w")

        # --- 4. ЛЕНТА ОБЪЯВЛЕНИЙ ---
        self.feed_container = ctk.CTkFrame(self.scroll_frame, fg_color="transparent")
        self.feed_container.pack(fill="x", padx=16, pady=4)

        self.render_feed()

        # --- 5. НИЖНЯЯ НАВИГАЦИЯ (BOTTOM BAR) ---
        self.bottom_bar = ctk.CTkFrame(self.main_container, fg_color=self.COLOR_CARD_BG, height=60, corner_radius=0, border_width=1, border_color=self.COLOR_ACCENT)
        self.bottom_bar.pack(fill="x", side="bottom")

        nav_items = ["🏠", "❤️", "➕", "💬", "👤"]
        for item in nav_items:
            if item == "➕":
                btn = ctk.CTkButton(self.bottom_bar, text=item, width=44, height=44, corner_radius=22, fg_color=self.COLOR_ACCENT, hover_color="#520B01", text_color=self.COLOR_TEXT, font=("Arial", 18))
            else:
                btn = ctk.CTkButton(self.bottom_bar, text=item, width=40, height=40, fg_color="transparent", text_color=self.COLOR_TEXT, font=("Arial", 16))
            btn.pack(side="left", expand=True, pady=8)

    # --- ОТРИСОВКА НОВОГОДНЕЙ ШАПКИ ---
    def draw_santa_hat(self, canvas):
        """ Рисует красную новогоднюю шапку с белым помпоном и опушкой """
        # Красный конус колпака
        canvas.create_polygon(6, 16, 22, 2, 38, 16, fill="#D32F2F", outline="")
        # Загнутый кончик
        canvas.create_polygon(22, 2, 30, 4, 34, 10, fill="#B71C1C", outline="")
        # Белый пушистый помпон
        canvas.create_oval(31, 8, 39, 16, fill="#FFFFFF", outline="#E0E0E0")
        # Белая опушка снизу
        canvas.create_oval(2, 14, 42, 20, fill="#FFFFFF", outline="#E0E0E0")

    # --- ОТРИСОВКА И АНИМАЦИЯ ГИРЛЯНДЫ ---
    def draw_garland(self):
        """ Рисует провода и светодиодные лампочки """
        self.garland_bulbs = []
        points = []
        num_points = 21
        width = 420
        for i in range(num_points):
            x = i * (width / (num_points - 1))
            y = 6 + (8 if i % 2 != 0 else 0)
            points.extend([x, y])

        self.garland_canvas.create_line(points, fill="#0F1407", width=2, smooth=True)
        self.garland_canvas.create_line([p + (1 if idx % 2 == 0 else 1) for idx, p in enumerate(points)], fill="#1C260D", width=1.5, smooth=True)

        for i in range(1, num_points - 1):
            x = i * (width / (num_points - 1))
            y = 6 + (8 if i % 2 != 0 else 0)

            self.garland_canvas.create_rectangle(x - 2, y, x + 2, y + 4, fill="#0B0E05", outline="")

            color = random.choice(self.bulb_colors)
            glow = self.garland_canvas.create_oval(x - 6, y + 2, x + 6, y + 14, fill=color, outline="", state="hidden")
            bulb = self.garland_canvas.create_oval(x - 3, y + 3, x + 3, y + 11, fill=color, outline="#FFFFFF")

            self.garland_bulbs.append({
                "bulb": bulb,
                "glow": glow,
                "x": x,
                "y": y
            })

    def animate_garland(self):
        """ Динамическое мигание и переключение цветов лампочек """
        if not hasattr(self, 'garland_canvas') or not self.garland_canvas.winfo_exists():
            return

        for bulb_info in self.garland_bulbs:
            if random.random() > 0.3:
                new_color = random.choice(self.bulb_colors)
                self.garland_canvas.itemconfig(bulb_info["bulb"], fill=new_color)
                self.garland_canvas.itemconfig(bulb_info["glow"], fill=new_color, state="normal")
            else:
                self.garland_canvas.itemconfig(bulb_info["glow"], state="hidden")

        self.after(350, self.animate_garland)

    def animate_snow(self):
        """ Движение снежинок """
        if not hasattr(self, 'snow_canvas') or not self.snow_canvas.winfo_exists():
            return
        for flake in self.snowflakes:
            flake["y"] += flake["speed"]
            if flake["y"] > 130:
                flake["y"] = -5
                flake["x"] = random.randint(0, 380)
            self.snow_canvas.coords(flake["id"], flake["x"], flake["y"], flake["x"] + flake["size"], flake["y"] + flake["size"])
        
        self.after(50, self.animate_snow)

    def delete_ad(self, ad_id):
        """ Функция модерации для администратора """
        if messagebox.askyesno("Удаление объявления", f"Удалить объявление ID #{ad_id}?"):
            self.ads_data = [ad for ad in self.ads_data if ad["id"] != ad_id]
            self.render_feed()

    def render_feed(self):
        for widget in self.feed_container.winfo_children():
            widget.destroy()

        if not self.ads_data:
            ctk.CTkLabel(self.feed_container, text="Нет доступных объявлений ❄", font=("Arial", 13), text_color=self.COLOR_TEXT).pack(pady=20)
            return

        for ad in self.ads_data:
            # Карточка
            card = ctk.CTkFrame(self.feed_container, fg_color=self.COLOR_CARD_BG, corner_radius=16, border_width=1, border_color=self.COLOR_ACCENT)
            card.pack(fill="x", pady=8)

            # Картинка-заглушка
            img_placeholder = ctk.CTkFrame(card, fg_color=self.COLOR_BG, height=100, corner_radius=12, border_width=1, border_color=self.COLOR_ACCENT)
            img_placeholder.pack(fill="x", padx=8, pady=8)

            # Новогодний бейдж
            badge = ctk.CTkLabel(
                img_placeholder, text=ad["badge"], 
                fg_color=self.COLOR_ACCENT, text_color=self.COLOR_TEXT, 
                corner_radius=6, font=("Arial", 9, "bold")
            )
            badge.pack(anchor="nw", padx=8, pady=8)

            # Инфо
            info_frame = ctk.CTkFrame(card, fg_color="transparent")
            info_frame.pack(fill="x", padx=12, pady=(0, 10))

            ctk.CTkLabel(info_frame, text=ad["category"], font=("Arial", 10, "bold"), text_color=self.COLOR_TEXT).pack(anchor="w")

            title_row = ctk.CTkFrame(info_frame, fg_color="transparent")
            title_row.pack(fill="x")

            ctk.CTkLabel(title_row, text=ad["title"], font=("Arial", 13, "bold"), text_color=self.COLOR_TEXT).pack(side="left")
            ctk.CTkLabel(title_row, text=ad["price"], font=("Arial", 14, "bold"), text_color=self.COLOR_TEXT).pack(side="right")

            loc_time = f"📍 {ad['location']}  •  🕒 {ad['time']}"
            ctk.CTkLabel(info_frame, text=loc_time, font=("Arial", 10), text_color=self.COLOR_TEXT).pack(anchor="w", pady=2)

            seller_row = ctk.CTkFrame(info_frame, fg_color="transparent")
            seller_row.pack(fill="x", pady=(6, 0))

            ctk.CTkLabel(seller_row, text=f"👤 {ad['seller']}", font=("Arial", 11), text_color=self.COLOR_TEXT).pack(side="left")
            ctk.CTkLabel(seller_row, text=ad["rating"], font=("Arial", 11, "bold"), text_color=self.COLOR_TEXT).pack(side="right")

            # Кнопка «Удалить» для роли администратора
            if self.current_role == "admin":
                delete_btn = ctk.CTkButton(
                    info_frame,
                    text="🗑 Удалить объявление (Админ)",
                    fg_color=self.COLOR_ACCENT,
                    hover_color="#520B01",
                    text_color=self.COLOR_TEXT,
                    height=28,
                    corner_radius=8,
                    font=("Arial", 10, "bold"),
                    command=lambda a_id=ad["id"]: self.delete_ad(a_id)
                )
                delete_btn.pack(fill="x", pady=(8, 0))


if __name__ == "__main__":
    app = NewYearMarketApp()
    app.mainloop()