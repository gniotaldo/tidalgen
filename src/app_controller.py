import tkinter as tk
from scenes.login import LoginScene
from scenes.main_menu import MainMenuScene
from scenes.playlist_lister import PlaylistListerScene
from scenes.playlist_preview import PlaylistPreviewScene
from scenes.tagging import TaggingScene

class AppController(tk.Tk):
    def __init__(self, state):
        super().__init__()

        self.state = state
        self.frames = {}
        self.current_frame = None
        self.title("Tidal Playlist Tool")
        self.geometry("700x800")

        container = tk.Frame(self)
        container.pack(fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.register_frame("login", LoginScene, container)
        self.register_frame("main_menu", MainMenuScene, container)
        self.register_frame("playlist_lister", PlaylistListerScene, container)
        self.register_frame("playlist_preview", PlaylistPreviewScene, container)
        self.register_frame("tagging", TaggingScene, container)

        self.show_frame("login")

    def register_frame(self, name, frame_class, container):
        frame = frame_class(parent=container, controller=self) 
        self.frames[name] = frame
        frame.grid(row=0, column=0, sticky="nsew")

    def show_frame(self, name):
        frame = self.frames.get(name)
        if frame:
            frame.tkraise()
            self.current_frame = frame
        else:
            print(f"[AppController] Frame '{name}' not found.")
