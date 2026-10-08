import customtkinter as ctk
from tkinter import messagebox
import db

class AuthWindow:
    def __init__(self, parent_container, on_login_success_callback, colors):
        self.container = parent_container
        self.on_login_success = on_login_success_callback
        self.COLORS = colors
        self.is_register_mode = False

        self.build_ui()

    def build_ui(self):
        for w in self.container.winfo_children():
            w.destroy()

        self.frame = ctk.CTkFrame(self.container, fg_color=self.COLORS["CARD_BG"], corner_radius=16, border_width=1, border_color=self.COLORS["ACCENT"])
        self.frame.pack(padx=20, pady=60, fill="both", expand=True)

        self.title_label = ctk.CTkLabel(
            self.frame, 
            text="Авторизация ❄️" if not self.is_register_mode else "Регистрация 🎄", 
            font=("Arial", 18, "bold"), 
            text_color=self.COLORS["TEXT"]
        )
        self.title_label.pack(pady=(20, 15))

        self.entry_login = ctk.CTkEntry(
            self.frame, placeholder_text="Логин",
            fg_color=self.COLORS["BG"], text_color=self.COLORS["TEXT"], border_color=self.COLORS["ACCENT"]
        )
        self.entry_login.pack(fill="x", padx=20, pady=6)

        self.entry_password = ctk.CTkEntry(
            self.frame, placeholder_text="Пароль", show="*",
            fg_color=self.COLORS["BG"], text_color=self.COLORS["TEXT"], border_color=self.COLORS["ACCENT"]
        )
        self.entry_password.pack(fill="x", padx=20, pady=6)

        if self.is_register_mode:
            self.entry_name = ctk.CTkEntry(
                self.frame, placeholder_text="ФИО / Имя",
                fg_color=self.COLORS["BG"], text_color=self.COLORS["TEXT"], border_color=self.COLORS["ACCENT"]
            )
            self.entry_name.pack(fill="x", padx=20, pady=6)

            self.entry_email = ctk.CTkEntry(
                self.frame, placeholder_text="Email",
                fg_color=self.COLORS["BG"], text_color=self.COLORS["TEXT"], border_color=self.COLORS["ACCENT"]
            )
            self.entry_email.pack(fill="x", padx=20, pady=6)

            self.role_var = ctk.StringVar(value="student")
            self.role_switch = ctk.CTkSegmentedButton(
                self.frame, values=["Студент", "Админ"],
                selected_color=self.COLORS["ACCENT"],
                unselected_color=self.COLORS["BG"],
                text_color=self.COLORS["TEXT"],
                command=self.on_role_change
            )
            self.role_switch.set("Студент")
            self.role_switch.pack(fill="x", padx=20, pady=8)

        self.btn_submit = ctk.CTkButton(
            self.frame, 
            text="Войти" if not self.is_register_mode else "Зарегистрироваться",
            fg_color=self.COLORS["ACCENT"], hover_color="#520B01",
            text_color=self.COLORS["TEXT"], font=("Arial", 12, "bold"),
            command=self.handle_submit
        )
        self.btn_submit.pack(fill="x", padx=20, pady=(15, 8))

        self.btn_toggle = ctk.CTkButton(
            self.frame,
            text="Нет аккаунта? Зарегистрироваться" if not self.is_register_mode else "Уже есть аккаунт? Войти",
            fg_color="transparent", hover_color=self.COLORS["BG"],
            text_color=self.COLORS["TEXT"], font=("Arial", 10, "underline"),
            command=self.toggle_mode
        )
        self.btn_toggle.pack(pady=5)

    def on_role_change(self, value):
        self.role_var.set("admin" if value == "Админ" else "student")

    def toggle_mode(self):
        self.is_register_mode = not self.is_register_mode
        self.build_ui()

    def handle_submit(self):
        login = self.entry_login.get().strip()
        password = self.entry_password.get().strip()

        if not login or not password:
            messagebox.showwarning("Ошибка", "Заполните логин и пароль!")
            return

        if self.is_register_mode:
            name = self.entry_name.get().strip()
            email = self.entry_email.get().strip()
            role = self.role_var.get()

            if not name or not email:
                messagebox.showwarning("Ошибка", "Заполните имя и email!")
                return

            if db.register_user(login, password, name, email, role):
                db.authenticate(login, password)
                messagebox.showinfo("Успех", "Регистрация успешна!")
                self.on_login_success()
            else:
                messagebox.showerror("Ошибка", "Пользователь с таким логином уже существует!")
        else:
            if db.authenticate(login, password):
                self.on_login_success()
            else:
                messagebox.showerror("Ошибка", "Неверный логин или пароль!")