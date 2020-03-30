import tkinter as tk
from tkinter import font as tk_font
from UI.Login.login_layout import LoginPage
from UI.Register.resgister_layout import RegisterPage


class Main(tk.Tk):

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        self.title_font = tk_font.Font(family='Helvetica', size=18, weight="bold", slant="italic")

        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        for F in (LoginPage, RegisterPage):
            page_name = F.__name__
            frame = F(parent=container, controller=self)
            self.frames[page_name] = frame

            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("LoginPage")

    def show_frame(self, page_name):
        x_cordinate = self.winfo_rootx()
        y_cordinate = self.winfo_rooty()
        if page_name == "RegisterPage":
            self.geometry("{}x{}+{}+{}".format(500, 300, x_cordinate, y_cordinate))
        if page_name == "LoginPage":
            self.geometry("{}x{}+{}+{}".format(400, 250, x_cordinate, y_cordinate))
        frame = self.frames[page_name]
        frame.tkraise()


if __name__ == "__main__":
    app = Main()
    app.geometry("400x250")
    app.mainloop()