import tkinter as tk
from tkinter import font as tk_font
import command_manager
import threading
from UI.HomePage.home_page_layout import HomePage
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
        for F in (LoginPage, RegisterPage, HomePage):
            page_name = F.__name__
            frame = F(parent=container, controller=self)
            self.frames[page_name] = frame

            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("LoginPage")

    def show_frame(self, page_name, *args):
        x_cord = self.winfo_rootx()
        y_cord = self.winfo_rooty()
        frame = self.frames[page_name]
        frame.tkraise()
        if page_name == "RegisterPage":
            self.geometry("{}x{}+{}+{}".format(500, 300, x_cord, y_cord))
        if page_name == "LoginPage":
            self.geometry("{}x{}+{}+{}".format(400, 250, x_cord, y_cord))
        if page_name == "HomePage":
            self.geometry("{}x{}+{}+{}".format(800, 600, x_cord, y_cord))
            frame.assistant_speaks(message="Witaj {}, mów do mnie Zbyszek, w czym Ci mogę pomóc ???".format(args[0]))
            threading.Thread(target=command_manager.start_listening, args=([frame, args[1]]), daemon=True).start()


if __name__ == "__main__":
    app = Main()
    app.geometry("400x250")
    app.mainloop()
