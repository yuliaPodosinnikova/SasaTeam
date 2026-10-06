import customtkinter as ctk
import random
from tkinter import messagebox
import db
from auth import AuthWindow

ctk.set_appearance_mode("Dark")


class NewYearMarketApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("САСАТИМ ❄️")
        self.geometry("420x840")
        self.resizable(False, False)

        self.COLORS = {
            "BG": "#1E2A0E",          
            "ACCENT": "#7B180A",      
            "TEXT": "#D2C5AC",        
            "CARD_BG": "#17210B",     
            "CARD_BORDER": "#7B180A", 
            "SEARCH_BG": "#141C09"    
        }

        self.configure(fg_color=self.COLORS["BG"])

        self.bulb_colors = ["#00BFFF", "#FF0055", "#00FF66", "#FFD700", "#FF1E27"]
        self.garland_bulbs = []
        self.selected_category = "Все ❄️"

        self.main_container = ctk.CTkFrame(self, fg_color=self.COLORS["BG"], corner_radius=0)
        self.main_container.pack(fill="both", expand=True)

        self.show_auth_screen()

    def show_auth_screen(self):
        for w in self.main_container.winfo_children():
            w.destroy()
        AuthWindow(self.main_container, self.build_main_interface, self.COLORS)

    def build_main_interface(self):
        for widget in self.main_container.winfo_children():
            widget.destroy()

        # 1. Гирлянда
        self.garland_canvas = ctk.CTkCanvas(self.main_container, width=420, height=28, bg=self.COLORS["BG"], highlightthickness=0)
        self.garland_canvas.pack(fill="x", side="top")
        self.draw_garland()
        self.animate_garland()

        # 2. Шапка (Логотип "САСАТИМ")
        self.header_frame = ctk.CTkFrame(self.main_container, fg_color="transparent")
        self.header_frame.pack(fill="x", padx=14, pady=(2, 6))

        self.logo_box = ctk.CTkFrame(self.header_frame, fg_color="transparent")
        self.logo_box.pack(side="left")

        self.hat_canvas = ctk.CTkCanvas(self.logo_box, width=42, height=18, bg=self.COLORS["BG"], highlightthickness=0)
        self.hat_canvas.pack(side="top", anchor="w")

        # Шапка Деда Мороза
        self.hat_canvas.create_polygon(6, 15, 20, 2, 34, 15, fill="#7B180A", outline="")
        self.hat_canvas.create_oval(1, 12, 39, 18, fill="#FFFFFF", outline="")
        self.hat_canvas.create_oval(32, 2, 38, 8, fill="#FFFFFF", outline="")

        # Кнопка САСАТИМ
        self.logo_btn = ctk.CTkButton(
            self.logo_box, text="САСАТИМ ❄️", width=110, height=36, 
            corner_radius=10, fg_color=self.COLORS["ACCENT"], hover_color="#520B01", 
            text_color=self.COLORS["TEXT"], font=("Arial", 12, "bold"),
            command=self.build_main_interface
        )
        self.logo_btn.pack(side="top")

        # Правый блок шапки
        self.avatar_frame = ctk.CTkFrame(self.header_frame, fg_color="transparent")
        self.avatar_frame.pack(side="right", pady=(12, 0))

        role_title = "Админ 🔑" if db.current_user["data"]["role"] == "admin" else "Студент 🎓"
        ctk.CTkLabel(
            self.avatar_frame, text=role_title, fg_color=self.COLORS["ACCENT"], text_color=self.COLORS["TEXT"],
            corner_radius=12, font=("Arial", 11, "bold"), padx=10, pady=5
        ).pack(side="left", padx=(0, 6))

        ctk.CTkButton(
            self.avatar_frame, text="🚪", width=34, height=34, 
            corner_radius=10, fg_color=self.COLORS["ACCENT"], hover_color="#520B01", text_color=self.COLORS["TEXT"],
            font=("Arial", 12), command=self.show_auth_screen
        ).pack(side="left")

        # 3. Область прокрутки
        self.scroll_frame = ctk.CTkScrollableFrame(self.main_container, fg_color="transparent", corner_radius=0)
        self.scroll_frame.pack(fill="both", expand=True, padx=0, pady=0)

        # 4. Поле поиска
        self.search_frame = ctk.CTkFrame(self.scroll_frame, fg_color="transparent")
        self.search_frame.pack(fill="x", padx=14, pady=(4, 8))

        self.search_entry = ctk.CTkEntry(
            self.search_frame, 
            placeholder_text="🔍  Поиск по объявлениям...", 
            placeholder_text_color="#8C8373",
            height=40, 
            fg_color=self.COLORS["SEARCH_BG"], 
            text_color=self.COLORS["TEXT"], 
            border_color=self.COLORS["ACCENT"],
            border_width=1,
            corner_radius=12,
            font=("Arial", 12)
        )
        self.search_entry.pack(fill="x")
        self.search_entry.bind("<KeyRelease>", self.filter_feed)

        # 5. Снежный баннер
        self.banner_frame = ctk.CTkFrame(self.scroll_frame, fg_color=self.COLORS["CARD_BG"], corner_radius=14, border_width=1, border_color=self.COLORS["ACCENT"])
        self.banner_frame.pack(fill="x", padx=14, pady=4)

        self.snow_canvas = ctk.CTkCanvas(self.banner_frame, width=380, height=115, bg=self.COLORS["CARD_BG"], highlightthickness=0)
        self.snow_canvas.pack(fill="both", expand=True)

        banner_subtitle = "Только для студентов" if db.current_user["data"]["role"] == "student" else "🛡️ Режим Администратора"
        self.snow_canvas.create_text(16, 20, anchor="w", text=banner_subtitle, fill=self.COLORS["TEXT"], font=("Arial", 11, "bold"))
        self.snow_canvas.create_text(16, 46, anchor="w", text="Всё нужное для учёбы — рядом", fill=self.COLORS["TEXT"], font=("Arial", 15, "bold"))
        self.snow_canvas.create_text(16, 72, anchor="w", text="Покупайте, продавайте и обменивайтесь\nвнутри университета. Безопасно и быстро.", fill=self.COLORS["TEXT"], font=("Arial", 10))

        ctk.CTkButton(
            self.banner_frame, text="+ Подать объявление", 
            fg_color=self.COLORS["ACCENT"], hover_color="#520B01", text_color=self.COLORS["TEXT"],
            corner_radius=10, font=("Arial", 12, "bold"), height=36,
            command=self.open_create_ad_modal
        ).pack(anchor="w", padx=16, pady=(0, 12))

        self.snowflakes = []
        for _ in range(22):
            x, y = random.randint(0, 380), random.randint(0, 115)
            size, speed = random.randint(2, 4), random.uniform(1.0, 2.0)
            flake = self.snow_canvas.create_oval(x, y, x + size, y + size, fill=self.COLORS["TEXT"], outline="")
            self.snowflakes.append({"id": flake, "x": x, "y": y, "speed": speed, "size": size})
        self.animate_snow()

        # 6. Фильтры категорий
        self.cat_scroll = ctk.CTkScrollableFrame(self.scroll_frame, orientation="horizontal", height=42, fg_color="transparent")
        self.cat_scroll.pack(fill="x", padx=10, pady=8)

        for cat in db.categories_list:
            is_active = (cat == self.selected_category)
            btn = ctk.CTkButton(
                self.cat_scroll, 
                text=cat, 
                height=32,
                fg_color=self.COLORS["ACCENT"] if is_active else self.COLORS["CARD_BG"],
                hover_color="#520B01",
                text_color=self.COLORS["TEXT"],
                border_width=1,
                border_color=self.COLORS["ACCENT"],
                corner_radius=10,
                font=("Arial", 11, "bold" if is_active else "normal"),
                command=lambda c=cat: self.select_category(c)
            )
            btn.pack(side="left", padx=4)

        # Заголовки ленты
        ctk.CTkLabel(self.scroll_frame, text="Свежие предложения", font=("Arial", 10), text_color=self.COLORS["TEXT"]).pack(anchor="w", padx=14, pady=(4, 0))
        ctk.CTkLabel(self.scroll_frame, text="Лента объявлений", font=("Arial", 16, "bold"), text_color=self.COLORS["TEXT"]).pack(anchor="w", padx=14, pady=(0, 6))

        # 7. Лента объявлений
        self.feed_container = ctk.CTkFrame(self.scroll_frame, fg_color="transparent")
        self.feed_container.pack(fill="x", padx=14, pady=0)
        self.render_feed()

        # 8. Нижняя панель навигации
        self.bottom_bar = ctk.CTkFrame(self.main_container, fg_color=self.COLORS["CARD_BG"], height=58, corner_radius=0, border_width=1, border_color=self.COLORS["ACCENT"])
        self.bottom_bar.pack(fill="x", side="bottom")

        ctk.CTkButton(self.bottom_bar, text="🏠", width=40, height=40, fg_color="transparent", text_color=self.COLORS["TEXT"], font=("Arial", 18), command=self.build_main_interface).pack(side="left", expand=True, pady=6)
        ctk.CTkButton(self.bottom_bar, text="❤", width=40, height=40, fg_color="transparent", text_color=self.COLORS["TEXT"], font=("Arial", 16)).pack(side="left", expand=True, pady=6)
        
        # Центральная кнопка '+'
        ctk.CTkButton(self.bottom_bar, text="+", width=48, height=48, corner_radius=24, fg_color=self.COLORS["ACCENT"], hover_color="#520B01", text_color=self.COLORS["TEXT"], font=("Arial", 22, "bold"), command=self.open_create_ad_modal).pack(side="left", expand=True, pady=4)
        
        ctk.CTkButton(self.bottom_bar, text="💬", width=40, height=40, fg_color="transparent", text_color=self.COLORS["TEXT"], font=("Arial", 16)).pack(side="left", expand=True, pady=6)
        
        # Кнопка Профиля
        ctk.CTkButton(self.bottom_bar, text="👤", width=40, height=40, fg_color="transparent", text_color=self.COLORS["TEXT"], font=("Arial", 16), command=self.show_profile_screen).pack(side="left", expand=True, pady=6)

    def select_category(self, cat):
        self.selected_category = cat
        self.build_main_interface()

    def filter_feed(self, event=None):
        self.render_feed()

    def render_feed(self):
        for widget in self.feed_container.winfo_children():
            widget.destroy()

        search_query = self.search_entry.get().strip().lower() if hasattr(self, 'search_entry') else ""

        filtered_ads = []
        for ad in db.ads_data:
            match_cat = (self.selected_category == "Все ❄️" or ad["category"] == self.selected_category)
            match_search = (search_query in ad["title"].lower() or search_query in ad["description"].lower())
            if match_cat and match_search:
                filtered_ads.append(ad)

        if not filtered_ads:
            ctk.CTkLabel(self.feed_container, text="Объявления не найдены ❄️", font=("Arial", 12), text_color=self.COLORS["TEXT"]).pack(pady=20)
            return

        for ad in filtered_ads:
            card = ctk.CTkFrame(self.feed_container, fg_color=self.COLORS["CARD_BG"], corner_radius=14, border_width=1, border_color=self.COLORS["ACCENT"])
            card.pack(fill="x", pady=8)

            info_frame = ctk.CTkFrame(card, fg_color="transparent")
            info_frame.pack(fill="x", padx=12, pady=10)

            if ad.get("badge"):
                badge_frame = ctk.CTkFrame(info_frame, fg_color=self.COLORS["ACCENT"], corner_radius=6)
                badge_frame.pack(anchor="w", pady=(0, 8))
                ctk.CTkLabel(badge_frame, text=f" {ad['badge']} ", font=("Arial", 10, "bold"), text_color=self.COLORS["TEXT"]).pack(padx=6, pady=2)

            ctk.CTkLabel(info_frame, text=ad["category"], font=("Arial", 10, "bold"), text_color=self.COLORS["TEXT"]).pack(anchor="w")

            title_row = ctk.CTkFrame(info_frame, fg_color="transparent")
            title_row.pack(fill="x", pady=(2, 0))

            ctk.CTkLabel(title_row, text=ad["title"], font=("Arial", 13, "bold"), text_color=self.COLORS["TEXT"]).pack(side="left")
            ctk.CTkLabel(title_row, text=ad["price"], font=("Arial", 14, "bold"), text_color=self.COLORS["TEXT"]).pack(side="right")

            loc_time = f"🔑 {ad['location']}  •  🕒 {ad['time']}"
            ctk.CTkLabel(info_frame, text=loc_time, font=("Arial", 10), text_color=self.COLORS["TEXT"]).pack(anchor="w", pady=2)

            if ad.get("description"):
                ctk.CTkLabel(info_frame, text=ad["description"], font=("Arial", 10), text_color="#8C8373", wraplength=340, justify="left").pack(anchor="w", pady=2)

            seller_row = ctk.CTkFrame(info_frame, fg_color="transparent")
            seller_row.pack(fill="x", pady=(6, 0))

            ctk.CTkLabel(seller_row, text=f"👤 {ad['seller_name']}", font=("Arial", 11), text_color=self.COLORS["TEXT"]).pack(side="left")
            ctk.CTkLabel(seller_row, text=f"{ad['rating']}", font=("Arial", 11, "bold"), text_color=self.COLORS["TEXT"]).pack(side="right")

            if db.current_user["data"]["role"] == "admin":
                ctk.CTkButton(
                    info_frame, text="🗑 Удалить (Админ)", fg_color=self.COLORS["ACCENT"], hover_color="#520B01",
                    text_color=self.COLORS["TEXT"], height=26, corner_radius=8, font=("Arial", 10, "bold"),
                    command=lambda a_id=ad["id"]: self.delete_ad(a_id)
                ).pack(fill="x", pady=(8, 0))

    def show_profile_screen(self):
        for widget in self.scroll_frame.winfo_children():
            widget.destroy()

        profile_card = ctk.CTkFrame(self.scroll_frame, fg_color=self.COLORS["CARD_BG"], corner_radius=16, border_width=1, border_color=self.COLORS["ACCENT"])
        profile_card.pack(fill="x", padx=16, pady=10)

        ctk.CTkLabel(profile_card, text="👤 Личный кабинет", font=("Arial", 16, "bold"), text_color=self.COLORS["TEXT"]).pack(pady=(15, 10))

        u = db.current_user["data"]
        info_text = (
            f"ФИО:  {u['name']}\n"
            f"Email:  {u['email']}\n"
            f"Логин:  {db.current_user['login']}\n"
            f"Роль:  {'Администратор' if u['role'] == 'admin' else 'Студент'}\n"
            f"Дата регистрации:  {u['date']}"
        )
        ctk.CTkLabel(profile_card, text=info_text, font=("Arial", 11), text_color=self.COLORS["TEXT"], justify="left").pack(anchor="w", padx=20, pady=5)

        ctk.CTkLabel(self.scroll_frame, text="Мои объявления:", font=("Arial", 14, "bold"), text_color=self.COLORS["TEXT"]).pack(anchor="w", padx=16, pady=(15, 5))

        my_ads = [ad for ad in db.ads_data if ad["seller_login"] == db.current_user["login"]]

        if not my_ads:
            ctk.CTkLabel(self.scroll_frame, text="У вас нет опубликованных объявлений ❄️", font=("Arial", 11), text_color="#8C8373").pack(padx=16, pady=10)
        else:
            for ad in my_ads:
                card = ctk.CTkFrame(self.scroll_frame, fg_color=self.COLORS["CARD_BG"], corner_radius=12, border_width=1, border_color=self.COLORS["ACCENT"])
                card.pack(fill="x", padx=16, pady=6)

                content_box = ctk.CTkFrame(card, fg_color="transparent")
                content_box.pack(fill="x", padx=12, pady=10)

                ctk.CTkLabel(content_box, text=f"{ad['title']}", font=("Arial", 12, "bold"), text_color=self.COLORS["TEXT"]).pack(anchor="w")
                ctk.CTkLabel(content_box, text=f"Цена: {ad['price']}  •  Категория: {ad['category']}", font=("Arial", 10), text_color="#8C8373").pack(anchor="w", pady=2)

                btn_row = ctk.CTkFrame(content_box, fg_color="transparent")
                btn_row.pack(fill="x", pady=(6, 0))

                # Кнопки Редактировать и Удалить
                ctk.CTkButton(
                    btn_row, text="✏️ Редактировать", width=110, height=26, fg_color=self.COLORS["ACCENT"], hover_color="#520B01",
                    text_color=self.COLORS["TEXT"], font=("Arial", 10, "bold"),
                    command=lambda target_ad=ad: self.open_edit_ad_modal(target_ad)
                ).pack(side="left", padx=(0, 6))

                ctk.CTkButton(
                    btn_row, text="❌ Удалить", width=80, height=26, fg_color="#520B01", hover_color="#300000",
                    text_color=self.COLORS["TEXT"], font=("Arial", 10, "bold"),
                    command=lambda a_id=ad["id"]: self.delete_ad(a_id, from_profile=True)
                ).pack(side="left")

    def open_create_ad_modal(self):
        modal = ctk.CTkToplevel(self)
        modal.title("Подать объявление")
        modal.geometry("380x560")
        modal.resizable(False, False)
        modal.configure(fg_color=self.COLORS["BG"])
        modal.grab_set()

        ctk.CTkLabel(modal, text="🎄 Новое объявление", font=("Arial", 16, "bold"), text_color=self.COLORS["TEXT"]).pack(pady=12)

        form = ctk.CTkFrame(modal, fg_color=self.COLORS["CARD_BG"], corner_radius=12, border_width=1, border_color=self.COLORS["ACCENT"])
        form.pack(fill="both", expand=True, padx=16, pady=(0, 16))

        ctk.CTkLabel(form, text="Название:", font=("Arial", 11, "bold"), text_color=self.COLORS["TEXT"]).pack(anchor="w", padx=12, pady=(10, 2))
        entry_title = ctk.CTkEntry(form, fg_color=self.COLORS["BG"], text_color=self.COLORS["TEXT"], border_color=self.COLORS["ACCENT"])
        entry_title.pack(fill="x", padx=12)

        ctk.CTkLabel(form, text="Категория:", font=("Arial", 11, "bold"), text_color=self.COLORS["TEXT"]).pack(anchor="w", padx=12, pady=(8, 2))
        combo_cat = ctk.CTkOptionMenu(form, values=[c for c in db.categories_list if c != "Все ❄️"], fg_color=self.COLORS["BG"], button_color=self.COLORS["ACCENT"], text_color=self.COLORS["TEXT"])
        combo_cat.pack(fill="x", padx=12)

        ctk.CTkLabel(form, text="Цена (₽):", font=("Arial", 11, "bold"), text_color=self.COLORS["TEXT"]).pack(anchor="w", padx=12, pady=(8, 2))
        entry_price = ctk.CTkEntry(form, fg_color=self.COLORS["BG"], text_color=self.COLORS["TEXT"], border_color=self.COLORS["ACCENT"])
        entry_price.pack(fill="x", padx=12)

        ctk.CTkLabel(form, text="Место встречи:", font=("Arial", 11, "bold"), text_color=self.COLORS["TEXT"]).pack(anchor="w", padx=12, pady=(8, 2))
        entry_loc = ctk.CTkEntry(form, fg_color=self.COLORS["BG"], text_color=self.COLORS["TEXT"], border_color=self.COLORS["ACCENT"])
        entry_loc.pack(fill="x", padx=12)

        def save():
            t, p, l = entry_title.get().strip(), entry_price.get().strip(), entry_loc.get().strip()
            if not (t and p and l):
                messagebox.showwarning("Ошибка", "Заполните все поля!", parent=modal)
                return

            # Исправлена генерация уникального ID
            new_id = max([ad["id"] for ad in db.ads_data], default=0) + 1

            db.ads_data.insert(0, {
                "id": new_id,
                "title": t,
                "category": combo_cat.get(),
                "price": p if "₽" in p else f"{p} ₽",
                "location": l,
                "time": "Только что",
                "seller_login": db.current_user["login"],
                "seller_name": db.current_user["data"]["name"],
                "rating": "5.0 ★",
                "badge": "Новое ❄️️",
                "description": ""
            })
            db.save_data() # Сохранение изменений в JSON
            modal.destroy()
            self.render_feed()

        ctk.CTkButton(form, text="Опубликовать", fg_color=self.COLORS["ACCENT"], hover_color="#520B01", text_color=self.COLORS["TEXT"], font=("Arial", 12, "bold"), command=save).pack(fill="x", padx=12, pady=15)

    def open_edit_ad_modal(self, ad):
        modal = ctk.CTkToplevel(self)
        modal.title("Редактировать объявление")
        modal.geometry("380x560")
        modal.resizable(False, False)
        modal.configure(fg_color=self.COLORS["BG"])
        modal.grab_set()

        ctk.CTkLabel(modal, text="✏️ Редактирование", font=("Arial", 16, "bold"), text_color=self.COLORS["TEXT"]).pack(pady=12)

        form = ctk.CTkFrame(modal, fg_color=self.COLORS["CARD_BG"], corner_radius=12, border_width=1, border_color=self.COLORS["ACCENT"])
        form.pack(fill="both", expand=True, padx=16, pady=(0, 16))

        ctk.CTkLabel(form, text="Название:", font=("Arial", 11, "bold"), text_color=self.COLORS["TEXT"]).pack(anchor="w", padx=12, pady=(10, 2))
        entry_title = ctk.CTkEntry(form, fg_color=self.COLORS["BG"], text_color=self.COLORS["TEXT"], border_color=self.COLORS["ACCENT"])
        entry_title.pack(fill="x", padx=12)
        entry_title.insert(0, ad["title"])

        ctk.CTkLabel(form, text="Категория:", font=("Arial", 11, "bold"), text_color=self.COLORS["TEXT"]).pack(anchor="w", padx=12, pady=(8, 2))
        combo_cat = ctk.CTkOptionMenu(form, values=[c for c in db.categories_list if c != "Все ❄️"], fg_color=self.COLORS["BG"], button_color=self.COLORS["ACCENT"], text_color=self.COLORS["TEXT"])
        combo_cat.pack(fill="x", padx=12)
        combo_cat.set(ad["category"])

        ctk.CTkLabel(form, text="Цена (₽):", font=("Arial", 11, "bold"), text_color=self.COLORS["TEXT"]).pack(anchor="w", padx=12, pady=(8, 2))
        entry_price = ctk.CTkEntry(form, fg_color=self.COLORS["BG"], text_color=self.COLORS["TEXT"], border_color=self.COLORS["ACCENT"])
        entry_price.pack(fill="x", padx=12)
        entry_price.insert(0, ad["price"].replace(" ₽", ""))

        ctk.CTkLabel(form, text="Место встречи:", font=("Arial", 11, "bold"), text_color=self.COLORS["TEXT"]).pack(anchor="w", padx=12, pady=(8, 2))
        entry_loc = ctk.CTkEntry(form, fg_color=self.COLORS["BG"], text_color=self.COLORS["TEXT"], border_color=self.COLORS["ACCENT"])
        entry_loc.pack(fill="x", padx=12)
        entry_loc.insert(0, ad["location"])

        def update():
            t, p, l = entry_title.get().strip(), entry_price.get().strip(), entry_loc.get().strip()
            if not (t and p and l):
                messagebox.showwarning("Ошибка", "Заполните все поля!", parent=modal)
                return
            ad["title"] = t
            ad["category"] = combo_cat.get()
            ad["price"] = p if "₽" in p else f"{p} ₽"
            ad["location"] = l
            
            db.save_data() # Сохранение изменений в JSON
            modal.destroy()
            messagebox.showinfo("Успех", "Объявление обновлено!")
            self.show_profile_screen()

        ctk.CTkButton(form, text="Сохранить изменения", fg_color=self.COLORS["ACCENT"], hover_color="#520B01", text_color=self.COLORS["TEXT"], font=("Arial", 12, "bold"), command=update).pack(fill="x", padx=12, pady=15)

    def delete_ad(self, ad_id, from_profile=False):
        if messagebox.askyesno("Удаление", f"Удалить объявление #{ad_id}?"):
            db.ads_data = [a for a in db.ads_data if a["id"] != ad_id]
            db.save_data() # Сохранение после удаления
            if from_profile:
                self.show_profile_screen()
            else:
                self.render_feed()

    def draw_garland(self):
        self.garland_bulbs = []
        points = []
        num_points = 21
        width = 420
        for i in range(num_points):
            x = i * (width / (num_points - 1))
            y = 5 + (6 if i % 2 != 0 else 0)
            points.extend([x, y])

        self.garland_canvas.create_line(points, fill="#0F1407", width=2, smooth=True)

        for i in range(1, num_points - 1):
            x = i * (width / (num_points - 1))
            y = 5 + (6 if i % 2 != 0 else 0)
            color = random.choice(self.bulb_colors)
            glow = self.garland_canvas.create_oval(x - 5, y + 2, x + 5, y + 12, fill=color, outline="", state="hidden")
            bulb = self.garland_canvas.create_oval(x - 3, y + 3, x + 3, y + 9, fill=color, outline="#FFFFFF")
            self.garland_bulbs.append({"bulb": bulb, "glow": glow})

    def animate_garland(self):
        if not hasattr(self, 'garland_canvas') or not self.garland_canvas.winfo_exists():
            return
        for b in self.garland_bulbs:
            if random.random() > 0.3:
                c = random.choice(self.bulb_colors)
                self.garland_canvas.itemconfig(b["bulb"], fill=c)
                self.garland_canvas.itemconfig(b["glow"], fill=c, state="normal")
            else:
                self.garland_canvas.itemconfig(b["glow"], state="hidden")
        self.after(350, self.animate_garland)

    def animate_snow(self):
        if not hasattr(self, 'snow_canvas') or not self.snow_canvas.winfo_exists():
            return
        for f in self.snowflakes:
            f["y"] += f["speed"]
            if f["y"] > 115:
                f["y"] = -5
                f["x"] = random.randint(0, 380)
            self.snow_canvas.coords(f["id"], f["x"], f["y"], f["x"] + f["size"], f["y"] + f["size"])
        self.after(50, self.animate_snow)


if __name__ == "__main__":
    app = NewYearMarketApp()
    app.mainloop()