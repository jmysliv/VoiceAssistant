import tkinter as tk
import text_to_speech
import threading

class HomePage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.row_counter = 1

    def assistant_doesnt_understand(self):
        tk.Label(self, text="Nie rozumiem, możesz powtórzyć?", font=("Helvetica", 9), bg="light grey").grid(row=self.row_counter, column=0,sticky="w", padx=5, pady=3)
        self.row_counter += 1
        threading.Thread(target=text_to_speech.speak, args=(["Nie rozumiem, możesz powtórzyć"]), daemon=True).start()

    def assistant_listening(self):
        tk.Label(self, text="Słucham...", font=("Helvetica", 9), bg="light grey").grid(row=self.row_counter, column=0, sticky="w", padx=5, pady=3)
        self.row_counter += 1
        threading.Thread(target=text_to_speech.speak, args=(["Słucham"]), daemon=True).start()

    def assistant_speaks(self, message):
        if len(message) > 64:
            message = text_to_speech.insert_newlines(message)
        label = tk.Label(self, text="", font=("Helvetica", 9), bg="light grey")
        label.grid(row=self.row_counter, column=0, sticky="w", padx=5,pady=3)
        self.slowly_print_text(label=label, message=message)
        self.row_counter += 1
        threading.Thread(target=text_to_speech.speak, args=([message]), daemon=True).start()

    def user_speaks(self, message):
        label = tk.Label(self, text="", font=("Helvetica", 9), bg="light blue")
        label.grid(row=self.row_counter, column=1, sticky="w", padx=5,pady=3)
        self.slowly_print_text(label=label, message=message)
        self.row_counter += 1

    def slowly_print_text(self, label, message, counter=1):
        label.config(text=message[:counter])
        if counter < len(message):
            self.controller.after(50, lambda: self.slowly_print_text(label, message, counter + 1))








