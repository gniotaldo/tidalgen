import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
import requests
from io import BytesIO
import tidalapi

class TaggingScene(tk.Frame):
    GENRES = ["pop", "classic rock", "rap", "metal", "alt rock", "electronic", "other"]
    TEMPOS = ["very slow", "slow", "normal", "fast", "very fast"]
    TONES = ["heavy", "sharp", "bright", "dark", "warm", "mellow"]
    MOODS = ["happy", "sad", "mysterious", "confusing", "energic", "calm", "melancholic"]

    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.image_label = tk.Label(self)
        self.image_label.pack(pady=10)

        self.title_label = tk.Label(self, font=("Arial", 16, "bold"))
        self.title_label.pack()

        self.album_label = tk.Label(self, font=("Arial", 12))
        self.album_label.pack(pady=5)

        # Rating
        tk.Label(self, text="Rating (0-10):").pack()
        self.rating_entry = tk.Entry(self)
        self.rating_entry.pack()

        # Genres (multi)
        tk.Label(self, text="Genres:").pack()

        genre_frame = tk.Frame(self)
        genre_frame.pack(fill='x')

        genre_inner_frame = tk.Frame(genre_frame)
        genre_inner_frame.pack()

        self.genre_vars = {}
        for genre in self.GENRES:
            var = tk.BooleanVar()
            cb = tk.Checkbutton(genre_inner_frame, text=genre, variable=var)
            cb.pack(side="left", padx=5)
            self.genre_vars[genre] = var

        # Tempo
        tk.Label(self, text="Tempo:").pack()
        self.tempo_var = tk.StringVar()
        self.tempo_dropdown = ttk.Combobox(self, textvariable=self.tempo_var, values=self.TEMPOS, state="readonly")
        self.tempo_dropdown.pack()

        # Tone
        tk.Label(self, text="Tone:").pack()
        self.tone_var = tk.StringVar()
        self.tone_dropdown = ttk.Combobox(self, textvariable=self.tone_var, values=self.TONES, state="readonly")
        self.tone_dropdown.pack()

        # Mood (multi)
        tk.Label(self, text="Mood:").pack()

        mood_frame = tk.Frame(self)
        mood_frame.pack(fill='x')

        mood_inner_frame = tk.Frame(mood_frame)
        mood_inner_frame.pack()

        self.mood_vars = {}
        for mood in self.MOODS:
            var = tk.BooleanVar()
            cb = tk.Checkbutton(mood_inner_frame, text=mood, variable=var)
            cb.pack(side="left", padx=5)
            self.mood_vars[mood] = var


        # Comments
        tk.Label(self, text="Comments:").pack()
        self.comments_entry = tk.Text(self, height=4, width=40)
        self.comments_entry.pack(pady=5)

        # Buttons
        btn_frame = tk.Frame(self)
        btn_frame.pack(pady=10)
        tk.Button(btn_frame, text="Save & Continue", command=self.save_and_continue).pack(side="left", padx=10)
        tk.Button(btn_frame, text="Save & Exit", command=self.save_and_exit).pack(side="right", padx=10)

    def load_next_track(self):
        state = self.controller.state
        if state.current_track_index >= len(state.current_playlist.tracks()):
            messagebox.showinfo("Done", "All tracks tagged!")
            return

        self.clear_fields()

        track = state.current_playlist.tracks()[state.current_track_index]
        self.title_label.config(text=f"{track.artist.name} - {track.name}")
        self.album_label.config(text=f"Album: {track.album.name}")

        try:
            img_url = track.album.image(640)
            response = requests.get(img_url)
            pil_img = Image.open(BytesIO(response.content)).resize((150, 150), Image.Resampling.LANCZOS)
            img = ImageTk.PhotoImage(pil_img)
            self.image_label.config(image=img)
            self.image_label.image = img
        except:
            self.image_label.config(image='', text='[No image]')

    def collect_data(self):
        track: tidalapi.Track = self.controller.state.current_playlist.tracks()[self.controller.state.current_track_index]
        return {
            "track_index": self.controller.state.current_track_index,
            "track_id": track.id,
            "track_name": track.name,
            "artist_name": track.artist.name,
            "album_name": track.album.name,
            "rating": self.rating_entry.get(),
            "genres": [g for g, var in self.genre_vars.items() if var.get()],
            "tempo": self.tempo_var.get(),
            "tone": self.tone_var.get(),
            "mood": [m for m, var in self.mood_vars.items() if var.get()],
            "comments": self.comments_entry.get("1.0", "end").strip(),
        }

    def save_state(self):
        try:
            self.controller.state.save_to_file("appstate.json")
            print("[TaggingScene] State saved")
        except Exception as e:
            print(f"[TaggingScene] Error saving state: {e}")

    def save_and_continue(self):
        self.save()
        self.load_next_track()

    def save_and_exit(self):
        self.save()
        self.controller.quit()

    def save(self):
        self.controller.state.tagged_tracks.append(self.collect_data())
        self.controller.state.current_track_index += 1
        self.save_state()

    def clear_fields(self):
        self.rating_entry.delete(0, tk.END)
        for var in self.genre_vars.values():
            var.set(False)
        self.tempo_var.set('')
        self.tone_var.set('')
        for var in self.mood_vars.values():
            var.set(False)
        self.comments_entry.delete("1.0", tk.END)
