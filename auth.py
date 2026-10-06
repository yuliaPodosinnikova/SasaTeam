import customtkinter as ctk
from tkinter import messagebox
from datetime import datetime
import db

class AuthWindow(ctk.CTkFrame):
    def __init__(self, parent, on_login_success, colors):
        super().__init__(parent, fg_color=colors["BG"], corner_radius=0)
        self.parent = parent
        self.on_login_success = on_login_success
        self.COLOR = colors

        self.pack(fill="both", expand=True)

        self.card = ctk.CTkFrame(
            self, 
            fg_color=self.COLOR["CARD_BG"], 
            corner_radius=20, 
            border_width=1, 
            border_color=self.COLOR["ACCENT"]
        )
        self.card.pack(fill="both", expand=True, padx=24, pady=40)

        ctk.CTkLabel(self.card, text="❄️", font=("Arial", 36), text_color=self.COLOR["TEXT"]).pack(pady=(20, 0))
        ctk.CTkLabel(self.card, text="САСАТИМ", font=("Arial", 20, "bold"), text_color=self.COLOR["TEXT"]).pack()

        self.auth_tab = ctk.CTkSegmentedButton(
            self.card,
            values=["Вход", "Регистрация"],
            command=self.switch_tab,
            selected_color=self.COLOR["ACCENT"],
            selected_hover_color="#520B01",
            unselected_color=self.COLOR["BG"],
            unselected_hover_color=self.COLOR["ACCENT"],
            text_color=self.COLOR["TEXT"],
            height=34
        )
        self.auth_tab.set("Вход")
        self.auth_tab.pack(fill="x", padx=20, pady=15)

        self.form_frame = ctk.CTkFrame(self.card, fg_color="transparent")
        self.form_frame.pack(fill="both", expand=True, padx=20, pady=5)

        self.render_login()

    def switch_tab(self, value):
        for w in self.form_frame.winfo_children():
            w.destroy()
        if value == "Вход":
            self.render_login()
        else:
            self.render_register()

    def render_login(self):
        ctk.CTkLabel(self.form_frame, text="Логин:", font=("Arial", 11, "bold"), text_color=self.COLOR["TEXT"]).pack(anchor="w")
        self.entry_login = ctk.CTkEntry(self.form_frame, placeholder_text="student или admin", height=38, fg_color=self.COLOR["BG"], text_color=self.COLOR["TEXT"], border_color=self.COLOR["ACCENT"])
        self.entry_login.pack(fill="x", pady=(2, 10))

        ctk.CTkLabel(self.form_frame, text="Пароль:", font=("Arial", 11, "bold"), text_color=self.COLOR["TEXT"]).pack(anchor="w")
        self.entry_pass = ctk.CTkEntry(self.form_frame, placeholder_text="Пароль...", show="*", height=38, fg_color=self.COLOR["BG"], text_color=self.COLOR["TEXT"], border_color=self.COLOR["ACCENT"])
        self.entry_pass.pack(fill="x", pady=(2, 15))

        ctk.CTkButton(
            self.form_frame, text="Войти", fg_color=self.COLOR["ACCENT"], hover_color="#520B01",
            text_color=self.COLOR["TEXT"], height=40, corner_radius=10, font=("Arial", 12, "bold"),
            command=self.handle_login
        ).pack(fill="x", pady=10)

        ctk.CTkLabel(self.form_frame, text="Тестовые аккаунты:\nСтудент: student / 123\nАдмин: admin / admin123", font=("Arial", 10), text_color="#8C8373").pack(pady=10)

    def render_register(self):
        ctk.CTkLabel(self.form_frame, text="Имя и Фамилия:", font=("Arial", 10, "bold"), text_color=self.COLOR["TEXT"]).pack(anchor="w")
        self.reg_name = ctk.CTkEntry(self.form_frame, placeholder_text="Иван И.", height=34, fg_color=self.COLOR["BG"], text_color=self.COLOR["TEXT"], border_color=self.COLOR["ACCENT"])
        self.reg_name.pack(fill="x", pady=(1, 4))

        ctk.CTkLabel(self.form_frame, text="Университетский Email:", font=("Arial", 10, "bold"), text_color=self.COLOR["TEXT"]).pack(anchor="w")
        self.reg_email = ctk.CTkEntry(self.form_frame, placeholder_text="student@univ.edu", height=34, fg_color=self.COLOR["BG"], text_color=self.COLOR["TEXT"], border_color=self.COLOR["ACCENT"])
        self.reg_email.pack(fill="x", pady=(1, 4))

        ctk.CTkLabel(self.form_frame, text="Логин:", font=("Arial", 10, "bold"), text_color=self.COLOR["TEXT"]).pack(anchor="w")
        self.reg_login = ctk.CTkEntry(self.form_frame, placeholder_text="Придумайте логин...", height=34, fg_color=self.COLOR["BG"], text_color=self.COLOR["TEXT"], border_color=self.COLOR["ACCENT"])
        self.reg_login.pack(fill="x", pady=(1, 4))

        ctk.CTkLabel(self.form_frame, text="Пароль:", font=("Arial", 10, "bold"), text_color=self.COLOR["TEXT"]).pack(anchor="w")
        self.reg_pass = ctk.CTkEntry(self.form_frame, placeholder_text="Придумайте пароль...", show="*", height=34, fg_color=self.COLOR["BG"], text_color=self.COLOR["TEXT"], border_color=self.COLOR["ACCENT"])
        self.reg_pass.pack(fill="x", pady=(1, 4))

        ctk.CTkLabel(self.form_frame, text="Роль:", font=("Arial", 10, "bold"), text_color=self.COLOR["TEXT"]).pack(anchor="w")
        self.reg_role = ctk.CTkOptionMenu(self.form_frame, values=["Студент 🎓", "Администратор 🔑"], fg_color=self.COLOR["BG"], button_color=self.COLOR["ACCENT"], text_color=self.COLOR["TEXT"], height=32)
        self.reg_role.pack(fill="x", pady=(1, 10))

        ctk.CTkButton(
            self.form_frame, text="Зарегистрироваться", fg_color=self.COLOR["ACCENT"], hover_color="#520B01",
            text_color=self.COLOR["TEXT"], height=38, corner_radius=10, font=("Arial", 12, "bold"),
            command=self.handle_register
        ).pack(fill="x", pady=5)

    def handle_login(self):
        login = self.entry_login.get().strip()
        password = self.entry_pass.get().strip()

        if login in db.users_db and db.users_db[login]["password"] == password:
            db.current_user["login"] = login
            db.current_user["data"] = db.users_db[login]
            self.on_login_success()
        else:
            messagebox.showerror("Ошибка", "Неверный логин или пароль!")

    def handle_register(self):
        name = self.reg_name.get().strip()
        email = self.reg_email.get().strip()
        login = self.reg_login.get().strip()
        password = self.reg_pass.get().strip()
        role = "admin" if "Администратор" in self.reg_role.get() else "student"

        if not (name and email and login and password):
            messagebox.showwarning("Внимание", "Заполните все поля!")
            return

        if login in db.users_db:
            messagebox.showerror("Ошибка", "Этот логин уже существует!")
            return

        db.users_db[login] = {
            "password": password,
            "role": role,
            "name": name,
            "email": email,
            "date": datetime.now().strftime("%d.%m.%Y")
        }

        db.save_data() # Сохраняем нового пользователя в файл
        db.current_user["login"] = login
        db.current_user["data"] = db.users_db[login]
        messagebox.showinfo("Успех", "Регистрация прошла успешно!")
        self.on_login_success()