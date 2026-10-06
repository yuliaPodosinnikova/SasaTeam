import customtkinter as ctk
from tkinter import messagebox
import db

class AuthWindow:
    def __init__(self, parent_frame, on_success_callback, colors):
        self.parent = parent_frame
        self.on_success = on_success_callback
        self.COLORS = colors
        self.show_login_screen()

    def show_login_screen(self):
        for w in self.parent.winfo_children():
            w.destroy()

        frame = ctk.CTkFrame(self.parent, fg_color=self.COLORS["CARD_BG"], corner_radius=16, border_width=1, border_color=self.COLORS["ACCENT"])
        frame.pack(expand=True, padx=20, pady=40, fill="both")

        ctk.CTkLabel(frame, text="❄️ Авторизация", font=("Arial", 18, "bold"), text_color=self.COLORS["TEXT"]).pack(pady=(20, 15))

        self.login_entry = ctk.CTkEntry(frame, placeholder_text="Логин", fg_color=self.COLORS["BG"], text_color=self.COLORS["TEXT"], border_color=self.COLORS["ACCENT"])
        self.login_entry.pack(fill="x", padx=20, pady=6)

        self.pass_entry = ctk.CTkEntry(frame, placeholder_text="Пароль", show="*", fg_color=self.COLORS["BG"], text_color=self.COLORS["TEXT"], border_color=self.COLORS["ACCENT"])
        self.pass_entry.pack(fill="x", padx=20, pady=6)

        ctk.CTkButton(frame, text="Войти", fg_color=self.COLORS["ACCENT"], hover_color="#520B01", text_color=self.COLORS["TEXT"], font=("Arial", 12, "bold"), command=self.do_login).pack(fill="x", padx=20, pady=(15, 6))
        ctk.CTkButton(frame, text="Регистрация", fg_color="transparent", text_color=self.COLORS["TEXT"], command=self.show_reg_screen).pack(pady=4)

    def show_reg_screen(self):
        for w in self.parent.winfo_children():
            w.destroy()

        frame = ctk.CTkFrame(self.parent, fg_color=self.COLORS["CARD_BG"], corner_radius=16, border_width=1, border_color=self.COLORS["ACCENT"])
        frame.pack(expand=True, padx=20, pady=20, fill="both")

        ctk.CTkLabel(frame, text="📝 Регистрация", font=("Arial", 18, "bold"), text_color=self.COLORS["TEXT"]).pack(pady=(15, 10))

        self.reg_login = ctk.CTkEntry(frame, placeholder_text="Логин", fg_color=self.COLORS["BG"], text_color=self.COLORS["TEXT"], border_color=self.COLORS["ACCENT"])
        self.reg_login.pack(fill="x", padx=20, pady=4)

        self.reg_pass = ctk.CTkEntry(frame, placeholder_text="Пароль", show="*", fg_color=self.COLORS["BG"], text_color=self.COLORS["TEXT"], border_color=self.COLORS["ACCENT"])
        self.reg_pass.pack(fill="x", padx=20, pady=4)

        self.reg_name = ctk.CTkEntry(frame, placeholder_text="Имя и Фамилия", fg_color=self.COLORS["BG"], text_color=self.COLORS["TEXT"], border_color=self.COLORS["ACCENT"])
        self.reg_name.pack(fill="x", padx=20, pady=4)

        self.reg_email = ctk.CTkEntry(frame, placeholder_text="Email", fg_color=self.COLORS["BG"], text_color=self.COLORS["TEXT"], border_color=self.COLORS["ACCENT"])
        self.reg_email.pack(fill="x", padx=20, pady=4)

        ctk.CTkButton(frame, text="Зарегистрироваться", fg_color=self.COLORS["ACCENT"], hover_color="#520B01", text_color=self.COLORS["TEXT"], font=("Arial", 12, "bold"), command=self.do_register).pack(fill="x", padx=20, pady=(12, 4))
        ctk.CTkButton(frame, text="Назад к входу", fg_color="transparent", text_color=self.COLORS["TEXT"], command=self.show_login_screen).pack(pady=4)

    def do_login(self):
        log = self.login_entry.get().strip()
        pwd = self.pass_entry.get().strip()
        if db.authenticate(log, pwd):
            self.on_success()
        else:
            messagebox.showerror("Ошибка", "Неверный логин или пароль!")

    def do_register(self):
        l, p, n, e = self.reg_login.get().strip(), self.reg_pass.get().strip(), self.reg_name.get().strip(), self.reg_email.get().strip()
        if not (l and p and n and e):
            messagebox.showwarning("Ошибка", "Заполните все поля!")
            return
        if db.register_user(l, p, n, e):
            messagebox.showinfo("Успех", "Регистрация успешна!")
            self.show_login_screen()
        else:
            messagebox.showerror("Ошибка", "Пользователь с таким логином уже существует!")