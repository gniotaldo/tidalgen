import tkinter as tk

class TaggingScene(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        tk.Label(self, text="Tagging", font=("Arial", 18)).pack(pady=30)
   