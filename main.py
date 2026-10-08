import customtkinter as ctk
import random
import os
from PIL import Image
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

        # 2. Шапка
        self.header_frame = ctk.CTkFrame(self.main_container, fg_color="transparent")
        self.header_frame.pack(fill="x", padx=14, pady=(2, 6))

        self.logo_box = ctk.CTkFrame(self.header_frame, fg_color="transparent")
        self.logo_box.pack(side="left")

        self.hat_canvas = ctk.CTkCanvas(self.logo_box, width=42, height=18, bg=self.COLORS["BG"], highlightthickness=0)
        self.hat_canvas.pack(side="top", anchor="w")

        self.hat_canvas.create_polygon(6, 15, 20, 2, 34, 15, fill="#7B180A", outline="")
        self.hat_canvas.create_oval(1, 12, 39, 18, fill="#FFFFFF", outline="")
        self.hat_canvas.create_oval(32, 2, 38, 8, fill="#FFFFFF", outline="")

        self.logo_btn = ctk.CTkButton(
            self.logo_box, text="САСАТИМ ❄️", width=110, height=36, 
            corner_radius=10, fg_color=self.COLORS["ACCENT"], hover_color="#520B01", 
            text_color=self.COLORS["TEXT"], font=("Arial", 12, "bold"),
            command=self.build_main_interface
        )
        self.logo_btn.pack(side="top")

        self.avatar_frame = ctk.CTkFrame(self.header_frame, fg_color="transparent")
        self.avatar_frame.pack(side="right", pady=(12, 0))

        role_title = "Админ 🔑" if db.current_user["data"]["role"] == "admin" else "Студент 🎓"
        ctk.CTkLabel(
            self.avatar_frame, text=role_title, fg_color=self.COLORS["ACCENT"], text_color=self.COLORS["TEXT"],
            corner_radius=12, font=("Arial", 11, "bold"), padx=10, pady=5
        ).pack(side="left", padx=(0, 6))

        if db.current_user["data"]["role"] == "admin":
            # Кнопка управления категориями для админа
            ctk.CTkButton(
                self.avatar_frame, text="📁", width=34, height=34, 
                corner_radius=10, fg_color=self.COLORS["ACCENT"], hover_color="#520B01", text_color="#FFFFFF",
                font=("Arial", 12), command=self.open_categories_modal
            ).pack(side="left", padx=(0, 4))

            # Кнопка управления пользователями
            ctk.CTkButton(
                self.avatar_frame, text="👥", width=34, height=34, 
                corner_radius=10, fg_color=self.COLORS["ACCENT"], hover_color="#520B01", text_color="#FFFFFF",
                font=("Arial", 12), command=self.open_users_modal
            ).pack(side="left", padx=(0, 4))

            # Кнопка статистики
            ctk.CTkButton(
                self.avatar_frame, text="📊", width=34, height=34, 
                corner_radius=10, fg_color=self.COLORS["ACCENT"], hover_color="#520B01", text_color="#FFFFFF",
                font=("Arial", 12), command=self.open_stats_modal
            ).pack(side="left", padx=(0, 4))

            # Кнопка жалоб
            ctk.CTkButton(
                self.avatar_frame, text="⚠️", width=34, height=34, 
                corner_radius=10, fg_color="#8B0000", hover_color="#520B01", text_color="#FFFFFF",
                font=("Arial", 12), command=self.open_reports_modal
            ).pack(side="left", padx=(0, 4))

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

        # 5. Баннер
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

        # 6. Фильтры
        self.cat_scroll = ctk.CTkScrollableFrame(self.scroll_frame, orientation="horizontal", height=42, fg_color="transparent")
        self.cat_scroll.pack(fill="x", padx=10, pady=8)

        categories_list = db.get_categories()
        if self.selected_category not in categories_list:
            self.selected_category = "Все ❄️"

        for cat in categories_list:
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

        ctk.CTkLabel(self.scroll_frame, text="Свежие предложения", font=("Arial", 10), text_color=self.COLORS["TEXT"]).pack(anchor="w", padx=14, pady=(4, 0))
        ctk.CTkLabel(self.scroll_frame, text="Лента объявлений", font=("Arial", 16, "bold"), text_color=self.COLORS["TEXT"]).pack(anchor="w", padx=14, pady=(0, 6))

        # 7. Лента объявлений
        self.feed_container = ctk.CTkFrame(self.scroll_frame, fg_color="transparent")
        self.feed_container.pack(fill="x", padx=14, pady=0)
        self.render_feed()

        # 8. Нижняя панель
        self.setup_bottom_bar()

    def setup_bottom_bar(self):
        self.bottom_bar = ctk.CTkFrame(self.main_container, fg_color=self.COLORS["CARD_BG"], height=58, corner_radius=0, border_width=1, border_color=self.COLORS["ACCENT"])
        self.bottom_bar.pack(fill="x", side="bottom")

        ctk.CTkButton(self.bottom_bar, text="🏠", width=40, height=40, fg_color="transparent", text_color=self.COLORS["TEXT"], font=("Arial", 18), command=self.build_main_interface).pack(side="left", expand=True, pady=6)
        ctk.CTkButton(self.bottom_bar, text="♥", width=40, height=40, fg_color="transparent", text_color=self.COLORS["TEXT"], font=("Arial", 18), command=self.show_favorites_screen).pack(side="left", expand=True, pady=6)
        ctk.CTkButton(self.bottom_bar, text="+", width=48, height=48, corner_radius=24, fg_color=self.COLORS["ACCENT"], hover_color="#520B01", text_color=self.COLORS["TEXT"], font=("Arial", 22, "bold"), command=self.open_create_ad_modal).pack(side="left", expand=True, pady=4)
        ctk.CTkButton(self.bottom_bar, text="💬", width=40, height=40, fg_color="transparent", text_color=self.COLORS["TEXT"], font=("Arial", 16), command=self.show_chats_screen).pack(side="left", expand=True, pady=6)
        ctk.CTkButton(self.bottom_bar, text="👤", width=40, height=40, fg_color="transparent", text_color=self.COLORS["TEXT"], font=("Arial", 16), command=self.show_profile_screen).pack(side="left", expand=True, pady=6)

    def select_category(self, cat):
        self.selected_category = cat
        self.build_main_interface()

    def filter_feed(self, event=None):
        self.render_feed()

    def render_feed(self, custom_ads=None):
        if not hasattr(self, 'feed_container') or not self.feed_container.winfo_exists():
            return

        for widget in self.feed_container.winfo_children():
            widget.destroy()

        search_query = self.search_entry.get().strip().lower() if hasattr(self, 'search_entry') and self.search_entry.winfo_exists() else ""
        
        all_ads = custom_ads if custom_ads is not None else db.get_all_ads()

        filtered_ads = []
        for ad in all_ads:
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

            top_row = ctk.CTkFrame(info_frame, fg_color="transparent")
            top_row.pack(fill="x", pady=(0, 4))

            if ad.get("badge"):
                badge_frame = ctk.CTkFrame(top_row, fg_color=self.COLORS["ACCENT"], corner_radius=6)
                badge_frame.pack(side="left", padx=(0, 6))
                ctk.CTkLabel(badge_frame, text=f" {ad['badge']} ", font=("Arial", 10, "bold"), text_color=self.COLORS["TEXT"]).pack(padx=4, pady=1)

            status = ad.get("status", "Активно")
            status_bg = "#2E8B57" if status == "Активно" else ("#D2691E" if status == "Забронировано" else "#708090")
            status_frame = ctk.CTkFrame(top_row, fg_color=status_bg, corner_radius=6)
            status_frame.pack(side="left")
            ctk.CTkLabel(status_frame, text=f" {status} ", font=("Arial", 10, "bold"), text_color="#FFFFFF").pack(padx=4, pady=1)

            is_fav = db.is_favorite(ad["id"])
            
            fav_btn = ctk.CTkButton(
                top_row, 
                text="♥" if is_fav else "♡", 
                text_color="#FF3B30" if is_fav else "#FFFFFF",
                fg_color="transparent",
                hover_color=self.COLORS["BG"],
                width=24, 
                height=24, 
                corner_radius=6,
                font=("Arial", 15, "bold")
            )
            fav_btn.configure(command=lambda a_id=ad["id"], btn=fav_btn: self.toggle_fav_action(a_id, btn))
            fav_btn.pack(side="right", padx=(2, 0))

            if ad["seller_login"] != db.current_user["login"]:
                ctk.CTkButton(
                    top_row, text="⚠️ Жалоба", width=60, height=20, fg_color="transparent",
                    text_color="#FF6347", font=("Arial", 10, "underline"), hover_color=self.COLORS["BG"],
                    command=lambda target_ad=ad: self.open_report_modal(target_ad)
                ).pack(side="right", padx=(0, 4))

            ctk.CTkLabel(info_frame, text=ad["category"], font=("Arial", 10, "bold"), text_color=self.COLORS["TEXT"]).pack(anchor="w", pady=(4, 0))

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

            ctk.CTkButton(
                seller_row,
                text=f"{ad['rating']}",
                font=("Arial", 11, "bold"),
                text_color="#FFD700",
                fg_color="transparent",
                hover_color=self.COLORS["BG"],
                height=20,
                width=40,
                command=lambda s_login=ad["seller_login"], s_name=ad["seller_name"]: self.open_seller_reviews_modal(s_login, s_name)
            ).pack(side="right")

            if ad["seller_login"] != db.current_user["login"]:
                ctk.CTkButton(
                    info_frame, 
                    text="💬 Написать продавцу", 
                    fg_color=self.COLORS["ACCENT"], 
                    hover_color="#520B01",
                    text_color=self.COLORS["TEXT"], 
                    height=28, 
                    corner_radius=8, 
                    font=("Arial", 11, "bold"),
                    command=lambda target_ad=ad: self.open_chat_modal(target_ad)
                ).pack(fill="x", pady=(8, 0))

            if db.current_user["data"]["role"] == "admin":
                ctk.CTkButton(
                    info_frame, text="🗑 Удалить (Админ)", fg_color=self.COLORS["ACCENT"], hover_color="#520B01",
                    text_color=self.COLORS["TEXT"], height=26, corner_radius=8, font=("Arial", 10, "bold"),
                    command=lambda a_id=ad["id"]: self.delete_ad(a_id)
                ).pack(fill="x", pady=(8, 0))

    def toggle_fav_action(self, ad_id, btn):
        is_fav = db.toggle_favorite(ad_id)
        if is_fav:
            btn.configure(text="♥", text_color="#FF3B30")
        else:
            btn.configure(text="♡", text_color="#FFFFFF")

    # МОДАЛЬНОЕ ОКНО УПРАВЛЕНИЯ КАТЕГОРИЯМИ ДЛЯ АДМИНА
    def open_categories_modal(self):
        modal = ctk.CTkToplevel(self)
        modal.title("Управление категориями")
        modal.geometry("380x500")
        modal.resizable(False, False)
        modal.configure(fg_color=self.COLORS["BG"])
        modal.grab_set()

        ctk.CTkLabel(modal, text="📁 Категории товаров", font=("Arial", 16, "bold"), text_color=self.COLORS["TEXT"]).pack(pady=(12, 6))

        # Форма добавления
        add_frame = ctk.CTkFrame(modal, fg_color=self.COLORS["CARD_BG"], corner_radius=12, border_width=1, border_color=self.COLORS["ACCENT"])
        add_frame.pack(fill="x", padx=14, pady=6)

        ctk.CTkLabel(add_frame, text="Добавить категорию:", font=("Arial", 11, "bold"), text_color=self.COLORS["TEXT"]).pack(anchor="w", padx=10, pady=(8, 4))
        
        entry_cat = ctk.CTkEntry(add_frame, placeholder_text="Например: 🎮 Игры", fg_color=self.COLORS["BG"], text_color=self.COLORS["TEXT"], border_color=self.COLORS["ACCENT"])
        entry_cat.pack(fill="x", padx=10, pady=(0, 8))

        def create_category():
            cat_name = entry_cat.get().strip()
            if not cat_name:
                messagebox.showwarning("Ошибка", "Введите название категории!", parent=modal)
                return
            if db.add_category(cat_name):
                entry_cat.delete(0, "end")
                refresh_list()
                self.build_main_interface()
                messagebox.showinfo("Успех", f"Категория '{cat_name}' добавлена!", parent=modal)
            else:
                messagebox.showerror("Ошибка", "Такая категория уже существует!", parent=modal)

        ctk.CTkButton(
            add_frame, text="+ Добавить", fg_color=self.COLORS["ACCENT"], hover_color="#520B01",
            text_color=self.COLORS["TEXT"], font=("Arial", 11, "bold"), height=28,
            command=create_category
        ).pack(fill="x", padx=10, pady=(0, 8))

        # Список действующих категорий
        ctk.CTkLabel(modal, text="Список категорий:", font=("Arial", 12, "bold"), text_color=self.COLORS["TEXT"]).pack(anchor="w", padx=14, pady=(8, 4))

        cats_scroll = ctk.CTkScrollableFrame(modal, fg_color="transparent")
        cats_scroll.pack(fill="both", expand=True, padx=10, pady=(0, 10))

        def refresh_list():
            for w in cats_scroll.winfo_children():
                w.destroy()

            current_cats = [c for c in db.get_categories() if c != "Все ❄️"]

            if not current_cats:
                ctk.CTkLabel(cats_scroll, text="Категорий пока нет ❄️", font=("Arial", 11), text_color="#8C8373").pack(pady=20)
                return

            for c_name in current_cats:
                card = ctk.CTkFrame(cats_scroll, fg_color=self.COLORS["CARD_BG"], corner_radius=8, border_width=1, border_color=self.COLORS["ACCENT"])
                card.pack(fill="x", pady=3)

                ctk.CTkLabel(card, text=c_name, font=("Arial", 11, "bold"), text_color=self.COLORS["TEXT"]).pack(side="left", padx=10, pady=6)

                def remove_cat(name=c_name):
                    if messagebox.askyesno("Удаление", f"Удалить категорию '{name}'?", parent=modal):
                        db.delete_category(name)
                        refresh_list()
                        self.build_main_interface()

                ctk.CTkButton(
                    card, text="🗑", width=28, height=24, fg_color="#8B0000", hover_color="#520B01",
                    text_color="#FFFFFF", font=("Arial", 11),
                    command=remove_cat
                ).pack(side="right", padx=6)

        refresh_list()

    # МОДАЛЬНОЕ ОКНО УПРАВЛЕНИЯ ПОЛЬЗОВАТЕЛЯМИ (АДМИН)
    def open_users_modal(self):
        modal = ctk.CTkToplevel(self)
        modal.title("Управление пользователями")
        modal.geometry("400x550")
        modal.resizable(False, False)
        modal.configure(fg_color=self.COLORS["BG"])
        modal.grab_set()

        ctk.CTkLabel(modal, text="👥 Пользователи системы", font=("Arial", 16, "bold"), text_color=self.COLORS["TEXT"]).pack(pady=10)

        scroll = ctk.CTkScrollableFrame(modal, fg_color="transparent")
        scroll.pack(fill="both", expand=True, padx=10, pady=(0, 10))

        def refresh_users():
            for w in scroll.winfo_children():
                w.destroy()

            users = db.get_all_users()
            for u in users:
                card = ctk.CTkFrame(scroll, fg_color=self.COLORS["CARD_BG"], corner_radius=10, border_width=1, border_color=self.COLORS["ACCENT"])
                card.pack(fill="x", pady=4)

                top = ctk.CTkFrame(card, fg_color="transparent")
                top.pack(fill="x", padx=10, pady=(6, 2))

                ctk.CTkLabel(top, text=f"{u['name']} (@{u['login']})", font=("Arial", 11, "bold"), text_color=self.COLORS["TEXT"]).pack(side="left")

                role_var = ctk.StringVar(value="Админ" if u["role"] == "admin" else "Студент")

                def change_role(val, user_login=u["login"]):
                    new_role = "admin" if val == "Админ" else "student"
                    db.update_user_role(user_login, new_role)
                    messagebox.showinfo("Успех", f"Роль {user_login} изменена на {val}!", parent=modal)

                role_menu = ctk.CTkOptionMenu(
                    top, values=["Студент", "Админ"], variable=role_var, width=90, height=22,
                    fg_color=self.COLORS["BG"], button_color=self.COLORS["ACCENT"], text_color=self.COLORS["TEXT"],
                    command=change_role
                )
                role_menu.pack(side="right")

                info_str = f"Email: {u['email']} | Дата: {u['date']}"
                ctk.CTkLabel(card, text=info_str, font=("Arial", 9), text_color="#8C8373").pack(anchor="w", padx=10, pady=(0, 4))

                if u["login"] != db.current_user["login"]:
                    def remove_u(login=u["login"]):
                        if messagebox.askyesno("Удаление", f"Удалить пользователя '{login}' и все его данные?", parent=modal):
                            db.delete_user(login)
                            refresh_users()
                            self.build_main_interface()

                    ctk.CTkButton(
                        card, text="🗑 Удалить аккаунт", height=22, fg_color="#8B0000", hover_color="#520B01",
                        text_color="#FFFFFF", font=("Arial", 9, "bold"), command=remove_u
                    ).pack(anchor="e", padx=10, pady=(0, 6))

        refresh_users()

    # МОДАЛЬНОЕ ОКНО СТАТИСТИКИ (АДМИН)
    def open_stats_modal(self):
        modal = ctk.CTkToplevel(self)
        modal.title("Статистика платформы")
        modal.geometry("360x480")
        modal.resizable(False, False)
        modal.configure(fg_color=self.COLORS["BG"])
        modal.grab_set()

        ctk.CTkLabel(modal, text="📊 Общая статистика", font=("Arial", 16, "bold"), text_color=self.COLORS["TEXT"]).pack(pady=12)

        stats = db.get_app_stats()

        container = ctk.CTkFrame(modal, fg_color=self.COLORS["CARD_BG"], corner_radius=14, border_width=1, border_color=self.COLORS["ACCENT"])
        container.pack(fill="both", expand=True, padx=16, pady=(0, 16))

        stats_data = [
            ("👥 Всего пользователей:", stats["users"]),
            ("🎓  • Студентов:", stats["students"]),
            ("🔑  • Администраторов:", stats["admins"]),
            ("📦 Всего объявлений:", stats["ads"]),
            ("🟢  • Активных:", stats["active_ads"]),
            ("🤝  • Проданных:", stats["sold_ads"]),
            ("📁 Категорий:", stats["categories"]),
            ("💬 Отзывов отправлено:", stats["reviews"]),
            ("⚠️ Жалоб в системе:", stats["reports"])
        ]

        for label, val in stats_data:
            row = ctk.CTkFrame(container, fg_color="transparent")
            row.pack(fill="x", padx=14, pady=4)

            font_weight = "bold" if not label.startswith(" ") else "normal"
            ctk.CTkLabel(row, text=label, font=("Arial", 11, font_weight), text_color=self.COLORS["TEXT"]).pack(side="left")
            ctk.CTkLabel(row, text=str(val), font=("Arial", 11, "bold"), text_color="#FFD700" if "•" not in label else self.COLORS["TEXT"]).pack(side="right")

    def show_chats_screen(self):
        for widget in self.scroll_frame.winfo_children():
            widget.destroy()

        ctk.CTkLabel(self.scroll_frame, text="Мои переписки", font=("Arial", 10), text_color=self.COLORS["TEXT"]).pack(anchor="w", padx=16, pady=(10, 0))
        ctk.CTkLabel(self.scroll_frame, text="Чаты 💬", font=("Arial", 18, "bold"), text_color=self.COLORS["TEXT"]).pack(anchor="w", padx=16, pady=(0, 10))

        user_chats = db.get_user_chats(db.current_user["login"])

        if not user_chats:
            ctk.CTkLabel(self.scroll_frame, text="У вас пока нет активных чатов ❄️\nНажмите «Написать продавцу» в объявлении!", font=("Arial", 11), text_color="#8C8373", justify="center").pack(pady=40)
            return

        for chat in user_chats:
            card = ctk.CTkFrame(self.scroll_frame, fg_color=self.COLORS["CARD_BG"], corner_radius=12, border_width=1, border_color=self.COLORS["ACCENT"])
            card.pack(fill="x", padx=16, pady=6)

            top_row = ctk.CTkFrame(card, fg_color="transparent")
            top_row.pack(fill="x", padx=10, pady=(8, 2))

            ctk.CTkLabel(top_row, text=f"👤 {chat['other_name']}", font=("Arial", 12, "bold"), text_color=self.COLORS["TEXT"]).pack(side="left")
            ctk.CTkLabel(top_row, text=chat["last_date"], font=("Arial", 9), text_color="#8C8373").pack(side="right")

            ctk.CTkLabel(card, text=f"📦 Товар: {chat['ad_title']}", font=("Arial", 10, "bold"), text_color=self.COLORS["TEXT"]).pack(anchor="w", padx=10)
            ctk.CTkLabel(card, text=f"«{chat['last_message']}»", font=("Arial", 10), text_color="#8C8373", wraplength=340, justify="left").pack(anchor="w", padx=10, pady=(2, 8))

            target_ad = db.get_ad_by_id(chat["ad_id"])
            if not target_ad:
                target_ad = {
                    "id": chat["ad_id"],
                    "title": chat["ad_title"],
                    "price": chat["ad_price"],
                    "seller_login": chat["other_login"],
                    "seller_name": chat["other_name"]
                }

            ctk.CTkButton(
                card, 
                text="Открыть диалог ➤", 
                height=26, 
                fg_color=self.COLORS["ACCENT"], 
                hover_color="#520B01",
                text_color=self.COLORS["TEXT"], 
                font=("Arial", 10, "bold"),
                command=lambda a=target_ad: self.open_chat_modal(a)
            ).pack(fill="x", padx=10, pady=(0, 8))

    def open_chat_modal(self, ad):
        modal = ctk.CTkToplevel(self)
        modal.title(f"Чат по товару: {ad['title']}")
        modal.geometry("380x500")
        modal.resizable(False, False)
        modal.configure(fg_color=self.COLORS["BG"])
        modal.grab_set()

        other_seller = ad.get('seller_name', 'Продавец')
        ctk.CTkLabel(
            modal, 
            text=f"💬 Чат: {other_seller}", 
            font=("Arial", 14, "bold"), 
            text_color=self.COLORS["TEXT"]
        ).pack(pady=(10, 2))
        
        ctk.CTkLabel(
            modal, 
            text=f"Товар: {ad['title']} ({ad.get('price', '')})", 
            font=("Arial", 10), 
            text_color="#8C8373"
        ).pack(pady=(0, 8))

        scroll_chat = ctk.CTkScrollableFrame(modal, fg_color=self.COLORS["CARD_BG"], corner_radius=10)
        scroll_chat.pack(fill="both", expand=True, padx=12, pady=5)

        other_login = ad["seller_login"] if ad["seller_login"] != db.current_user["login"] else "student"

        def load_messages():
            for w in scroll_chat.winfo_children():
                w.destroy()
            
            messages = db.get_chat_messages(db.current_user["login"], other_login, ad["id"])
            
            if not messages:
                ctk.CTkLabel(
                    scroll_chat, 
                    text="Начните диалог с продавцом ❄️", 
                    font=("Arial", 10), 
                    text_color="#8C8373"
                ).pack(pady=20)
                return

            for msg in messages:
                is_me = (msg["sender_login"] == db.current_user["login"])
                align = "e" if is_me else "w"
                bg_col = self.COLORS["ACCENT"] if is_me else self.COLORS["BG"]

                msg_box = ctk.CTkFrame(scroll_chat, fg_color=bg_col, corner_radius=8)
                msg_box.pack(anchor=align, pady=4, padx=6)

                ctk.CTkLabel(
                    msg_box, 
                    text=msg["text"], 
                    font=("Arial", 10), 
                    text_color=self.COLORS["TEXT"], 
                    wraplength=220, 
                    justify="left"
                ).pack(padx=8, pady=4)

        load_messages()

        input_frame = ctk.CTkFrame(modal, fg_color="transparent")
        input_frame.pack(fill="x", padx=12, pady=10)

        entry_msg = ctk.CTkEntry(
            input_frame, 
            placeholder_text="Напишите сообщение...", 
            fg_color=self.COLORS["CARD_BG"], 
            text_color=self.COLORS["TEXT"], 
            border_color=self.COLORS["ACCENT"]
        )
        entry_msg.pack(side="left", fill="x", expand=True, padx=(0, 6))

        def send_msg():
            txt = entry_msg.get().strip()
            if not txt:
                return
            db.send_message(
                sender_login=db.current_user["login"],
                receiver_login=other_login,
                ad_id=ad["id"],
                text=txt
            )
            entry_msg.delete(0, "end")
            load_messages()

        ctk.CTkButton(
            input_frame, 
            text="➤", 
            width=40, 
            fg_color=self.COLORS["ACCENT"], 
            hover_color="#520B01",
            text_color=self.COLORS["TEXT"],
            command=send_msg
        ).pack(side="right")

    def open_seller_reviews_modal(self, seller_login, seller_name):
        modal = ctk.CTkToplevel(self)
        modal.title("Отзывы продавца")
        modal.geometry("380x600")
        modal.resizable(False, False)
        modal.configure(fg_color=self.COLORS["BG"])
        modal.grab_set()

        avg_rating, count = db.get_seller_rating(seller_login)
        rating_str = f"{avg_rating:.1f} ★ ({count})" if count > 0 else "Нет оценок"

        ctk.CTkLabel(modal, text=f"Продавец: {seller_name}", font=("Arial", 15, "bold"), text_color=self.COLORS["TEXT"]).pack(pady=(12, 2))
        ctk.CTkLabel(modal, text=f"Рейтинг: {rating_str}", font=("Arial", 13, "bold"), text_color="#FFD700").pack(pady=(0, 10))

        if seller_login != db.current_user["login"]:
            form = ctk.CTkFrame(modal, fg_color=self.COLORS["CARD_BG"], corner_radius=10, border_width=1, border_color=self.COLORS["ACCENT"])
            form.pack(fill="x", padx=12, pady=(0, 10))

            ctk.CTkLabel(form, text="Оставить отзыв:", font=("Arial", 11, "bold"), text_color=self.COLORS["TEXT"]).pack(anchor="w", padx=10, pady=(6, 2))

            rate_row = ctk.CTkFrame(form, fg_color="transparent")
            rate_row.pack(fill="x", padx=10, pady=2)
            ctk.CTkLabel(rate_row, text="Оценка:", font=("Arial", 10), text_color=self.COLORS["TEXT"]).pack(side="left", padx=(0, 6))

            rating_var = ctk.StringVar(value="5")
            rating_combo = ctk.CTkOptionMenu(
                rate_row, values=["5", "4", "3", "2", "1"],
                variable=rating_var, width=60, height=22,
                fg_color=self.COLORS["BG"], button_color=self.COLORS["ACCENT"], text_color=self.COLORS["TEXT"]
            )
            rating_combo.pack(side="left")

            entry_comment = ctk.CTkEntry(form, placeholder_text="Напишите впечатления...", fg_color=self.COLORS["BG"], text_color=self.COLORS["TEXT"], border_color=self.COLORS["ACCENT"])
            entry_comment.pack(fill="x", padx=10, pady=6)

            def submit_review():
                comment = entry_comment.get().strip()
                if not comment:
                    messagebox.showwarning("Ошибка", "Заполните текст отзыва!", parent=modal)
                    return
                db.add_review(
                    seller_login=seller_login,
                    reviewer_login=db.current_user["login"],
                    reviewer_name=db.current_user["data"]["name"],
                    rating=int(rating_var.get()),
                    comment=comment
                )
                modal.destroy()
                messagebox.showinfo("Успех", "Отзыв успешно добавлен!")
                self.render_feed()

            ctk.CTkButton(
                form, text="Отправить отзыв", height=26,
                fg_color=self.COLORS["ACCENT"], hover_color="#520B01",
                text_color=self.COLORS["TEXT"], font=("Arial", 11, "bold"),
                command=submit_review
            ).pack(fill="x", padx=10, pady=(0, 8))

        ctk.CTkLabel(modal, text="Отзывы покупателей:", font=("Arial", 12, "bold"), text_color=self.COLORS["TEXT"]).pack(anchor="w", padx=14, pady=(2, 4))

        scroll = ctk.CTkScrollableFrame(modal, fg_color="transparent")
        scroll.pack(fill="both", expand=True, padx=10, pady=(0, 10))

        reviews = db.get_seller_reviews(seller_login)
        if not reviews:
            ctk.CTkLabel(scroll, text="У этого продавца пока нет отзывов ❄️", font=("Arial", 11), text_color="#8C8373").pack(pady=20)
        else:
            for r in reviews:
                card = ctk.CTkFrame(scroll, fg_color=self.COLORS["CARD_BG"], corner_radius=10, border_width=1, border_color=self.COLORS["ACCENT"])
                card.pack(fill="x", pady=4)

                top = ctk.CTkFrame(card, fg_color="transparent")
                top.pack(fill="x", padx=8, pady=(6, 2))

                ctk.CTkLabel(top, text=f"👤 {r['reviewer_name']}", font=("Arial", 10, "bold"), text_color=self.COLORS["TEXT"]).pack(side="left")
                ctk.CTkLabel(top, text=f"{'★' * r['rating']}", font=("Arial", 10), text_color="#FFD700").pack(side="right")

                ctk.CTkLabel(card, text=r["comment"], font=("Arial", 10), text_color=self.COLORS["TEXT"], wraplength=320, justify="left").pack(anchor="w", padx=8, pady=(0, 4))
                ctk.CTkLabel(card, text=r["date"], font=("Arial", 8), text_color="#8C8373").pack(anchor="e", padx=8, pady=(0, 4))

    def show_favorites_screen(self):
        for widget in self.scroll_frame.winfo_children():
            widget.destroy()

        ctk.CTkLabel(self.scroll_frame, text="Сохранённые товары", font=("Arial", 10), text_color=self.COLORS["TEXT"]).pack(anchor="w", padx=16, pady=(10, 0))
        ctk.CTkLabel(self.scroll_frame, text="Избранное ♥", font=("Arial", 18, "bold"), text_color=self.COLORS["TEXT"]).pack(anchor="w", padx=16, pady=(0, 10))

        fav_ads = db.get_user_favorites()

        if not fav_ads:
            ctk.CTkLabel(self.scroll_frame, text="У вас пока нет избранных объявлений ❄️", font=("Arial", 12), text_color="#8C8373").pack(pady=30)
            return

        self.feed_container = ctk.CTkFrame(self.scroll_frame, fg_color="transparent")
        self.feed_container.pack(fill="x", padx=14, pady=0)
        self.render_feed(custom_ads=fav_ads)

    def show_profile_screen(self):
        for widget in self.scroll_frame.winfo_children():
            widget.destroy()

        profile_card = ctk.CTkFrame(self.scroll_frame, fg_color=self.COLORS["CARD_BG"], corner_radius=16, border_width=1, border_color=self.COLORS["ACCENT"])
        profile_card.pack(fill="x", padx=16, pady=10)

        u = db.current_user["data"]
        avatar_path = os.path.join("assets", "пончик.jpg")

        if os.path.exists(avatar_path):
            img = Image.open(avatar_path)
            avatar_image = ctk.CTkImage(light_image=img, dark_image=img, size=(80, 80))
            avatar_label = ctk.CTkLabel(profile_card, image=avatar_image, text="")
            avatar_label.pack(pady=(15, 5))
        else:
            ctk.CTkLabel(profile_card, text="👤", font=("Arial", 40)).pack(pady=(15, 5))

        avg_rating, count = db.get_seller_rating(db.current_user["login"])
        rating_str = f"{avg_rating:.1f} ★ ({count})" if count > 0 else "Нет оценок"

        ctk.CTkLabel(profile_card, text=u['name'], font=("Arial", 16, "bold"), text_color=self.COLORS["TEXT"]).pack(pady=(0, 2))
        ctk.CTkLabel(profile_card, text=f"Мой рейтинг: {rating_str}", font=("Arial", 11, "bold"), text_color="#FFD700").pack(pady=(0, 10))

        info_text = (
            f"Email:  {u['email']}\n"
            f"Логин:  {db.current_user['login']}\n"
            f"Роль:  {'Администратор' if u['role'] == 'admin' else 'Студент'}\n"
            f"Дата регистрации:  {u['date']}"
        )
        ctk.CTkLabel(profile_card, text=info_text, font=("Arial", 11), text_color=self.COLORS["TEXT"], justify="left").pack(anchor="w", padx=20, pady=10)

        ctk.CTkLabel(self.scroll_frame, text="Отзывы обо мне:", font=("Arial", 14, "bold"), text_color=self.COLORS["TEXT"]).pack(anchor="w", padx=16, pady=(10, 5))
        
        my_reviews = db.get_seller_reviews(db.current_user["login"])
        if not my_reviews:
            ctk.CTkLabel(self.scroll_frame, text="Вам пока не оставляли отзывов ❄️", font=("Arial", 11), text_color="#8C8373").pack(padx=16, pady=5)
        else:
            for r in my_reviews:
                card = ctk.CTkFrame(self.scroll_frame, fg_color=self.COLORS["CARD_BG"], corner_radius=10, border_width=1, border_color=self.COLORS["ACCENT"])
                card.pack(fill="x", padx=16, pady=4)

                top = ctk.CTkFrame(card, fg_color="transparent")
                top.pack(fill="x", padx=8, pady=(6, 2))

                ctk.CTkLabel(top, text=f"👤 {r['reviewer_name']}", font=("Arial", 10, "bold"), text_color=self.COLORS["TEXT"]).pack(side="left")
                ctk.CTkLabel(top, text=f"{'★' * r['rating']}", font=("Arial", 10), text_color="#FFD700").pack(side="right")

                ctk.CTkLabel(card, text=r["comment"], font=("Arial", 10), text_color=self.COLORS["TEXT"], wraplength=340, justify="left").pack(anchor="w", padx=8, pady=(0, 4))

        ctk.CTkLabel(self.scroll_frame, text="Мои объявления:", font=("Arial", 14, "bold"), text_color=self.COLORS["TEXT"]).pack(anchor="w", padx=16, pady=(15, 5))

        all_ads = db.get_all_ads()
        my_ads = [ad for ad in all_ads if ad["seller_login"] == db.current_user["login"]]

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

                status_row = ctk.CTkFrame(content_box, fg_color="transparent")
                status_row.pack(fill="x", pady=(4, 6))

                ctk.CTkLabel(status_row, text="Статус:", font=("Arial", 10, "bold"), text_color=self.COLORS["TEXT"]).pack(side="left", padx=(0, 6))
                
                status_combo = ctk.CTkOptionMenu(
                    status_row, 
                    values=["Активно", "Забронировано", "Продано"],
                    fg_color=self.COLORS["BG"], button_color=self.COLORS["ACCENT"],
                    text_color=self.COLORS["TEXT"], height=24, width=130,
                    command=lambda new_st, a_id=ad["id"]: self.change_status(a_id, new_st)
                )
                status_combo.pack(side="left")
                status_combo.set(ad.get("status", "Активно"))

                btn_row = ctk.CTkFrame(content_box, fg_color="transparent")
                btn_row.pack(fill="x", pady=(6, 0))

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

    def change_status(self, ad_id, new_status):
        db.update_ad_status(ad_id, new_status)
        messagebox.showinfo("Успех", f"Статус объявления изменен на '{new_status}'!")

    def open_report_modal(self, ad):
        modal = ctk.CTkToplevel(self)
        modal.title("Жалоба")
        modal.geometry("340x300")
        modal.resizable(False, False)
        modal.configure(fg_color=self.COLORS["BG"])
        modal.grab_set()

        ctk.CTkLabel(modal, text="⚠️ Жалоба на объявление", font=("Arial", 14, "bold"), text_color=self.COLORS["TEXT"]).pack(pady=10)
        ctk.CTkLabel(modal, text=f"«{ad['title']}»", font=("Arial", 11), text_color="#8C8373").pack(pady=(0, 10))

        entry_reason = ctk.CTkTextbox(modal, height=100, fg_color=self.COLORS["CARD_BG"], text_color=self.COLORS["TEXT"], border_color=self.COLORS["ACCENT"], border_width=1)
        entry_reason.pack(fill="x", padx=16, pady=5)

        def send():
            reason = entry_reason.get("1.0", "end").strip()
            if not reason:
                messagebox.showwarning("Ошибка", "Укажите причину жалобы!", parent=modal)
                return
            db.add_report(ad["id"], db.current_user["login"], reason)
            modal.destroy()
            messagebox.showinfo("Успех", "Жалоба отправлена администратору!", parent=self)

        ctk.CTkButton(modal, text="Отправить", fg_color=self.COLORS["ACCENT"], hover_color="#520B01", text_color=self.COLORS["TEXT"], command=send).pack(pady=15)

    def open_reports_modal(self):
        modal = ctk.CTkToplevel(self)
        modal.title("Управление жалобами")
        modal.geometry("380x520")
        modal.resizable(False, False)
        modal.configure(fg_color=self.COLORS["BG"])
        modal.grab_set()

        ctk.CTkLabel(modal, text="🛡️ Жалобы пользователей", font=("Arial", 15, "bold"), text_color=self.COLORS["TEXT"]).pack(pady=10)

        scroll = ctk.CTkScrollableFrame(modal, fg_color="transparent")
        scroll.pack(fill="both", expand=True, padx=10, pady=5)

        reports = db.get_all_reports()

        if not reports:
            ctk.CTkLabel(scroll, text="Жалоб пока нет 🎉", font=("Arial", 12), text_color=self.COLORS["TEXT"]).pack(pady=20)
            return

        for r in reports:
            card = ctk.CTkFrame(scroll, fg_color=self.COLORS["CARD_BG"], corner_radius=10, border_width=1, border_color=self.COLORS["ACCENT"])
            card.pack(fill="x", pady=6)

            ctk.CTkLabel(card, text=f"Объявление: {r['ad_title']} (#{r['ad_id']})", font=("Arial", 11, "bold"), text_color=self.COLORS["TEXT"]).pack(anchor="w", padx=10, pady=(6, 2))
            ctk.CTkLabel(card, text=f"От: {r['reporter_login']}  •  Дата: {r['date']}", font=("Arial", 10), text_color="#8C8373").pack(anchor="w", padx=10)
            ctk.CTkLabel(card, text=f"Причина: {r['reason']}", font=("Arial", 10), text_color=self.COLORS["TEXT"], wraplength=320, justify="left").pack(anchor="w", padx=10, pady=4)

            btn_row = ctk.CTkFrame(card, fg_color="transparent")
            btn_row.pack(fill="x", padx=10, pady=(0, 6))

            def del_ad(ad_id=r['ad_id'], rep_id=r['report_id']):
                db.delete_ad(ad_id)
                modal.destroy()
                self.build_main_interface()
                messagebox.showinfo("Админ", "Объявление удалено!")

            def dismiss(rep_id=r['report_id']):
                db.delete_report(rep_id)
                modal.destroy()
                messagebox.showinfo("Админ", "Жалоба отклонена!")

            ctk.CTkButton(btn_row, text="🗑 Удалить объявление", fg_color="#520B01", text_color=self.COLORS["TEXT"], height=24, font=("Arial", 10), command=del_ad).pack(side="left", padx=(0, 5))
            ctk.CTkButton(btn_row, text="❌ Отклонить", fg_color=self.COLORS["BG"], text_color=self.COLORS["TEXT"], height=24, font=("Arial", 10), command=dismiss).pack(side="left")

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
        valid_cats = [c for c in db.get_categories() if c != "Все ❄️"]
        combo_cat = ctk.CTkOptionMenu(form, values=valid_cats, fg_color=self.COLORS["BG"], button_color=self.COLORS["ACCENT"], text_color=self.COLORS["TEXT"])
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

            p_formatted = p if "₽" in p else f"{p} ₽"
            db.add_ad(
                title=t,
                category=combo_cat.get(),
                price=p_formatted,
                location=l,
                seller_login=db.current_user["login"],
                seller_name=db.current_user["data"]["name"]
            )
            modal.destroy()
            self.build_main_interface()

        ctk.CTkButton(form, text="Опубликовать", fg_color=self.COLORS["ACCENT"], hover_color="#520B01", text_color=self.COLORS["TEXT"], font=("Arial", 12, "bold"), command=save).pack(fill="x", padx=12, pady=15)

    def open_edit_ad_modal(self, ad):
        modal = ctk.CTkToplevel(self)
        modal.title("Редактировать объявление")
        modal.geometry("380x560")
        modal.resizable(False, False)
        modal.configure(fg_color=self.COLORS["BG"])
        modal.grab_set()

        ctk.CTkLabel(modal, text="✏ Редактирование", font=("Arial", 16, "bold"), text_color=self.COLORS["TEXT"]).pack(pady=12)

        form = ctk.CTkFrame(modal, fg_color=self.COLORS["CARD_BG"], corner_radius=12, border_width=1, border_color=self.COLORS["ACCENT"])
        form.pack(fill="both", expand=True, padx=16, pady=(0, 16))

        ctk.CTkLabel(form, text="Название:", font=("Arial", 11, "bold"), text_color=self.COLORS["TEXT"]).pack(anchor="w", padx=12, pady=(10, 2))
        entry_title = ctk.CTkEntry(form, fg_color=self.COLORS["BG"], text_color=self.COLORS["TEXT"], border_color=self.COLORS["ACCENT"])
        entry_title.pack(fill="x", padx=12)
        entry_title.insert(0, ad["title"])

        ctk.CTkLabel(form, text="Категория:", font=("Arial", 11, "bold"), text_color=self.COLORS["TEXT"]).pack(anchor="w", padx=12, pady=(8, 2))
        valid_cats = [c for c in db.get_categories() if c != "Все ❄️"]
        combo_cat = ctk.CTkOptionMenu(form, values=valid_cats, fg_color=self.COLORS["BG"], button_color=self.COLORS["ACCENT"], text_color=self.COLORS["TEXT"])
        combo_cat.pack(fill="x", padx=12)
        if ad["category"] in valid_cats:
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
            p_formatted = p if "₽" in p else f"{p} ₽"
            db.update_ad(ad["id"], t, combo_cat.get(), p_formatted, l)
            modal.destroy()
            messagebox.showinfo("Успех", "Объявление обновлено!")
            self.show_profile_screen()

        ctk.CTkButton(form, text="Сохранить изменения", fg_color=self.COLORS["ACCENT"], hover_color="#520B01", text_color=self.COLORS["TEXT"], font=("Arial", 12, "bold"), command=update).pack(fill="x", padx=12, pady=15)

    def delete_ad(self, ad_id, from_profile=False):
        if messagebox.askyesno("Удаление", f"Удалить объявление #{ad_id}?"):
            db.delete_ad(ad_id)
            if from_profile:
                self.show_profile_screen()
            else:
                self.build_main_interface()

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