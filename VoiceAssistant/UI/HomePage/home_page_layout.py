import tkinter as tk
import time


class HomePage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.row_counter = 1

    def assistant_speaks(self, message):
        label = tk.Label(self, text="", font=("Helvetica", 9), bg="light grey")
        label.grid(row=self.row_counter, column=0, sticky="w", padx=5,pady=3)
        self.slowly_print_text(label=label, message=message)
        self.row_counter += 1

    def user_speaks(self, message):
        label = tk.Label(self, text="", font=("Helvetica", 9), bg="light blue")
        label.grid(row=self.row_counter, column=1, sticky="w", padx=5,pady=3)
        self.slowly_print_text(label=label, message=message)
        self.row_counter += 1

    def slowly_print_text(self, label, message, counter=1):
        label.config(text=message[:counter])
        if counter < len(message):
            self.controller.after(50, lambda: self.slowly_print_text(label, message, counter + 1))






