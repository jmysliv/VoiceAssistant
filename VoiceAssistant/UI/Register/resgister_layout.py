import tkinter as tk
from UI.Login.login_service import login


class RegisterPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        self.label_username = tk.Label(self, text="Username")
        self.label_email = tk.Label(self, text="Email")
        self.label_password = tk.Label(self, text="Password")
        self.label_conf_pass = tk.Label(self, text="Confirm Password")

        self.entry_username = tk.Entry(self)
        self.entry_email = tk.Entry(self, show="*")
        self.entry_password = tk.Entry(self)
        self.entry_conf_pass = tk.Entry(self, show="*")

        self.entry_username.bind('<Return>', lambda _: self._register_btn_clicked())
        self.entry_email.bind('<Return>', lambda _: self._register_btn_clicked())
        self.entry_password.bind('<Return>', lambda _: self._register_btn_clicked())
        self.entry_conf_pass.bind('<Return>', lambda _: self._register_btn_clicked())

        self.label_username.grid(row=0, sticky='E', padx=(80, 10), pady=(30, 0))
        self.label_email.grid(row=1, sticky='E', padx=(80, 10), pady=(10, 0))
        self.label_password.grid(row=2, sticky='E', padx=(80, 10), pady=(10, 0))
        self.label_conf_pass.grid(row=3, sticky='E', padx=(80, 10), pady=(10, 0))

        self.entry_username.grid(row=0, column=1, pady=(30, 0))
        self.entry_email.grid(row=1, column=1, pady=(10, 0))
        self.entry_password.grid(row=2, column=1, pady=(10, 0))
        self.entry_conf_pass.grid(row=3, column=1, pady=(10, 0))

        self.login_btn = tk.Button(self, text="Register", command=self._register_btn_clicked)
        self.login_btn.grid(row=4, column=0, sticky='E', padx=5, pady=(10, 0))

        self.login_btn = tk.Button(self, text="Back", command=lambda: controller.show_frame("LoginPage"))
        self.login_btn.grid(row=4, column=1, pady=(10, 0))

        self.message = tk.Label(self)
        self.message.grid(columnspan=2, pady=10, padx=10)
        self.message.place(x=270, y=230, anchor="center")

    def _register_btn_clicked(self):
        username = self.entry_username.get()
        password = self.entry_password.get()

        if login(username, password):
            self.message.config(text="Welcome " + username, fg="green")
        else:
            self.message.config(text="Invalid username or password!!!", fg="red")
