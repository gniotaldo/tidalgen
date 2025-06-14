import tkinter as tk

class PlaylistPreviewScene(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        tk.Label(self, text="Playlist Preview", font=("Arial", 18)).pack(pady=30)

    
