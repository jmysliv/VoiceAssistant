import time
import tkinter as tk
from UI.Login.login_service import login, validate


class LoginPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.label_username = tk.Label(self, text="Username")
        self.label_password = tk.Label(self, text="Password")

        self.entry_username = tk.Entry(self)
        self.entry_password = tk.Entry(self, show="*")

        self.entry_username.bind('<Return>', lambda _: self._login_btn_clicked())
        self.entry_password.bind('<Return>', lambda _: self._login_btn_clicked())

        self.label_username.grid(row=0, sticky='E', padx=(80, 10), pady=(30, 0))
        self.label_password.grid(row=1, sticky='E', padx=(80, 10), pady=(10, 0))

        self.entry_username.grid(row=0, column=1, pady=(30, 0))
        self.entry_password.grid(row=1, column=1, pady=(10, 0))

        self.login_btn = tk.Button(self, text="Zaloguj", command=self._login_btn_clicked)
        self.login_btn.grid(row=3, column=0, sticky='E', padx=5, pady=(10, 0))

        self.register_btn = tk.Button(self, text="Załóż konto", command=lambda: self.controller.show_frame("RegisterPage"))
        self.register_btn.grid(row=3, column=1, pady=(10, 0))

        self.message = tk.Label(self)
        self.message.grid(columnspan=2, pady=10, sticky='N')
        self.message.place(x=200, y=190, anchor="center")

    def _login_btn_clicked(self):
        username = self.entry_username.get()
        password = self.entry_password.get()

        validation_result = validate(username, password)
        if validation_result is not "ok":
            self.message.config(text=validation_result, fg="red")
            return
        else:
            message, token = login(username, password)
            if message is not "ok":
                self.message.config(text=message, fg="red")
            else:
                self.message.config(text="Poprawne logowanie", fg="green")
                self.controller.show_frame("HomePage", username, token)
