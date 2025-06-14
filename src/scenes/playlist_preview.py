import tkinter as tk
import tidalapi
from PIL import Image, ImageTk
import requests
from io import BytesIO

class PlaylistPreviewScene(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.images = []  # referencje do obrazków
        self.track_images = []  # osobne referencje dla tracków

        self.playlist_image_label = tk.Label(self)
        self.playlist_image_label.pack(pady=(10, 5))

        self.playlist_name_label = tk.Label(self, font=("Arial", 18, "bold"))
        self.playlist_name_label.pack(pady=(0, 10))

        self.canvas = tk.Canvas(self)
        self.scrollbar = tk.Scrollbar(self, orient="vertical", command=self.canvas.yview)
        
        self.inner_frame = tk.Frame(self.canvas)
        self.track_frame = tk.Frame(self.inner_frame)
        self.track_frame.pack(anchor="center")

        self.track_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )


        self.canvas.create_window((0, 0), window=self.inner_frame, anchor="n")

        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        self.canvas.pack(side="left", fill="both", expand=True)
        self.scrollbar.pack(side="right", fill="y")

    def load_playlist(self, playlist):
        # Czyścimy wcześniejsze widgety i obrazy
        for widget in self.track_frame.winfo_children():
            widget.destroy()
        self.images.clear()
        self.track_images.clear()

        # Obrazek playlisty
        try:
            img_url = playlist.image(dimensions=640)
            response = requests.get(img_url)
            pil_img = Image.open(BytesIO(response.content)).resize((50, 50), Image.Resampling.LANCZOS)
            img = ImageTk.PhotoImage(pil_img)
            self.playlist_image_label.configure(image=img)
            self.playlist_image_label.image = img  # zachowaj referencję
        except Exception as e:
            print(f"[PlaylistPreviewScene] Cannot load playlist image: {e}")
            self.playlist_image_label.configure(image='', text='[No image]')

        self.playlist_name_label.configure(text=playlist.name)

        # Załaduj tracki
        try:
            tracks = playlist.tracks()
        except Exception as e:
            print(f"[PlaylistPreviewScene] Failed to fetch tracks: {e}")
            return
        track: tidalapi.Track
        for track in tracks:
            frame = tk.Frame(self.track_frame, bd=1, relief="solid", padx=5, pady=5)
            frame.pack(fill="x", padx=10, pady=5)

            # Miniaturka albumu
            try:
                album_img_url = track.album.image(160)
                response = requests.get(album_img_url)
                pil_img = Image.open(BytesIO(response.content)).resize((60, 60), Image.Resampling.LANCZOS)
                img = ImageTk.PhotoImage(pil_img)
                self.track_images.append(img)
                img_label = tk.Label(frame, image=img)
                img_label.pack(side="left", padx=5)
            except Exception as e:
                print(f"[PlaylistPreviewScene] Cannot load album image: {e}")

            # Info o utworze
            text = f"{track.artist.name} - {track.name} {track.duration}"
            label = tk.Label(frame, text=text, font=("Arial", 12), anchor="w", justify="left")
            label.pack(side="left", fill="x", expand=True)
