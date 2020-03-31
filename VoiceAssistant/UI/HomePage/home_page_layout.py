import tkinter as tk


class HomePage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.username = ""
        self.l_text = tk.Label(self, text="")
        self.l_text.grid(row=0, column=0, sticky='E')

    def print_message(self, message, counter=1):
        self.l_text.config(text=message[:counter])
        self.controller.after(150, lambda: self.print_message(message, counter + 1))
