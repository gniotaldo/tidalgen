import tkinter as tk
from PIL import Image, ImageTk
import requests
from io import BytesIO
from core.playlist_scrapper import get_all_playlists

class PlaylistListerScene(tk.Frame):
    TILE_WIDTH = 120
    PADDING = 10
    
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.playlists = []
        self.images = []
        self.resize_job = None

        tk.Label(self, text="Choose Playlist", font=("Arial", 18)).pack(pady=10)

        self.canvas = tk.Canvas(self)
        scrollbar = tk.Scrollbar(self, orient="vertical", command=self.canvas.yview)
        self.frame = tk.Frame(self.canvas)

        self.frame.bind("<Configure>", lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))
        self.canvas.create_window((0, 0), window=self.frame, anchor="nw")
        self.canvas.configure(yscrollcommand=scrollbar.set)

        self.canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        self.bind("<Configure>", self.on_resize)

    def on_resize(self, event):
        if event.widget == self and self.playlists:
            if self.resize_job:
                self.after_cancel(self.resize_job)
            self.resize_job = self.after(300, self.render_playlists)

    def load_playlists(self):
        self.playlists = get_all_playlists(self.controller.state.session)

        self.render_playlists()

    def calculate_columns(self):
        width = self.winfo_width() or 600
        available_width = width - 20
        tile_total_width = self.TILE_WIDTH + (3 * self.PADDING) 
        return max(1, available_width // tile_total_width)

    def render_playlists(self):
        for widget in self.frame.winfo_children():
            widget.destroy()
        self.images.clear()

        if not self.playlists:
            return

        columns = self.calculate_columns()

        for i, playlist in enumerate(self.playlists):
            btn = self.create_playlist_button(playlist)
            row, col = divmod(i, columns)
            btn.grid(row=row, column=col, padx=self.PADDING, pady=self.PADDING)

        for col in range(columns):
            self.frame.grid_columnconfigure(col, weight=1)

    def create_playlist_button(self, playlist):
        img = self.load_playlist_image(playlist)
        
        if img:
            return tk.Button(
                self.frame,
                text=playlist.name,
                image=img,
                compound='top',
                font=("Arial", 12),
                width=self.TILE_WIDTH,
                height=140,
                wraplength=110,
                padx=5, pady=5,
                command=lambda: self.on_playlist_click(playlist)
            )
        else:
            return tk.Button(
                self.frame,
                text=playlist.name,
                font=("Arial", 12),
                width=15,
                height=7,
                wraplength=110,
                padx=5, pady=5
            )

    def load_playlist_image(self, playlist):
        try:
            response = requests.get(playlist.image(dimensions=160))
            pil_image = Image.open(BytesIO(response.content))
            pil_image = pil_image.resize((100, 100), Image.Resampling.LANCZOS)
            img = ImageTk.PhotoImage(pil_image)
            self.images.append(img)
            return img
        except Exception as e:
            print(f"[PlaylistListerScene] Failed to load image for playlist '{playlist.name}': {e}")
            return None
    def on_playlist_click(self, playlist):
        print(f"[PlaylistListerScene] Playlist '{playlist.name}' clicked.")
        self.controller.state.current_playlist = playlist
        if self.controller.state.is_tagging:
            # go to tagging scene
            tagging_scene = self.controller.frames.get("tagging")
            if tagging_scene:
                tagging_scene.load_next_track()
            self.controller.show_frame("tagging")
        else:
            # go to playlist preview scene
            playlist_scene = self.controller.frames.get("playlist_preview")
            if playlist_scene:
                playlist_scene.load_playlist(playlist)
            self.controller.show_frame("playlist_preview")