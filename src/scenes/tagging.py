import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
import requests
from io import BytesIO
import tidalapi
import ctypes
import time



class TaggingScene(tk.Frame):
    GENRES = [
        "pop",
        "classic rock",
        "hard rock",
        "alt rock",
        "grunge",
        "metal",
        "rap",
        "electronic",
        "eurodisco",
        "country",
        "new wave",
        "disco",
        "other"
    ]

    TEMPOS = [
        "very slow",
        "slow",
        "normal",
        "fast",
        "very fast"
    ]

    TONES = [
        "heavy",
        "sharp",
        "bright",
        "dark",
        "warm",
        "mellow",
        "aggressive",
        "dreamy"
    ]

    MOODS = [
        "happy",
        "sad",
        "calm",
        "energic",
        "melancholic",
        "mysterious",
        "nostalgic",
        "aggressive"
    ]

    VOCALS = [
        "instrumental",
        "male",
        "female",
        "group",
        "duet",
        "robotic",
        "minimal",
        "screaming"
    ]

    GUITAR_INTENSITY = [
        "none",
        "subtle",
        "strong",
        "dominant",
        "solo-hero"
    ]

    SYNTH_PRESENCE = [
        "none",
        "subtle",
        "dominant"
    ]

    PRODUCTION_STYLE = [
        "raw",
        "clean",
        "lo-fi",
        "modern",
        "retro",
        "wall-of-sound"
    ]

    ENERGY_LEVEL = [
        "low",
        "medium",
        "high",
        "explosive"
    ]

    USE_CASE = [
        "driving",
        "party",
        "chill",
        "workout",
        "football",
        "night",
        "focus",
        "beach"
    ]



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
        tk.Label(self, text="Rating (0-10):").pack(pady=(10,0))
        self.rating_entry = tk.Entry(self)
        self.rating_entry.pack(fill='x', padx=5, pady=2)

        def create_checkboxes(label, options, var_dict):
            tk.Label(self, text=label).pack(pady=(8,0))
            frame_outer = tk.Frame(self)
            frame_outer.pack(fill='x', padx=5)
            frame_inner = tk.Frame(frame_outer)
            frame_inner.pack()
            for opt in options:
                var = tk.BooleanVar()
                cb = tk.Checkbutton(frame_inner, text=opt, variable=var)
                cb.pack(side='left', padx=5, pady=2)
                var_dict[opt] = var

        # Genres
        self.genre_vars = {}
        create_checkboxes("Genres:", self.GENRES, self.genre_vars)

        # Tempo
        self.tempo_vars = {}
        create_checkboxes("Tempo:", self.TEMPOS, self.tempo_vars)

        # Tone
        self.tone_vars = {}
        create_checkboxes("Tone:", self.TONES, self.tone_vars)

        # Mood
        self.mood_vars = {}
        create_checkboxes("Mood:", self.MOODS, self.mood_vars)

        # Vocals
        self.vocals_vars = {}
        create_checkboxes("Vocals:", self.VOCALS, self.vocals_vars)

        # Guitar Intensity
        self.guitar_vars = {}
        create_checkboxes("Guitar Intensity:", self.GUITAR_INTENSITY, self.guitar_vars)

        # Synth Presence
        self.synth_vars = {}
        create_checkboxes("Synth Presence:", self.SYNTH_PRESENCE, self.synth_vars)

        # Production Style
        self.prod_vars = {}
        create_checkboxes("Production Style:", self.PRODUCTION_STYLE, self.prod_vars)

        # Energy Level
        self.energy_vars = {}
        create_checkboxes("Energy Level:", self.ENERGY_LEVEL, self.energy_vars)

        # Use Case
        self.usecase_vars = {}
        create_checkboxes("Use Case:", self.USE_CASE, self.usecase_vars)

        # Comments
        tk.Label(self, text="Comments:").pack(pady=(8,0))
        self.comments_entry = tk.Text(self, height=4, width=60)
        self.comments_entry.pack(fill='x', padx=5, pady=2)

        # Buttons
        btn_frame = tk.Frame(self)
        btn_frame.pack(pady=10)
        tk.Button(btn_frame, text="Save & Continue", command=self.save_and_continue).pack(side="left", padx=10)
        tk.Button(btn_frame, text="Save & Exit", command=self.save_and_exit).pack(side="right", padx=10)

        # Progress
        self.progress_label = tk.Label(self, text="Progress: 0/0")
        self.progress_label.pack(pady=5)

    

    def load_next_track(self):
        self.progress_label.config(text=f"Progress: {self.controller.app_state.current_track_index + 1}/{len(self.controller.app_state.current_playlist.tracks())}")
        state = self.controller.app_state
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
        track: tidalapi.Track = self.controller.app_state.current_playlist.tracks()[self.controller.app_state.current_track_index]
        return {
            "track_index":      self.controller.app_state.current_track_index,
            "track_id":         track.id,
            "track_name":       track.name,
            "artist_name":      track.artist.name,
            "album_name":       track.album.name,
            "rating":           self.rating_entry.get(),
            "genres":           [g for g, var in self.genre_vars.items() if var.get()],
            "tempo":            [t for t, var in self.tempo_vars.items() if var.get()],
            "tone":             [t for t, var in self.tone_vars.items() if var.get()],
            "mood":             [m for m, var in self.mood_vars.items() if var.get()],
            "vocals":           [v for v, var in self.vocals_vars.items() if var.get()],
            "guitar_intensity": [g for g, var in self.guitar_vars.items() if var.get()],
            "synth_presence":   [s for s, var in self.synth_vars.items() if var.get()],
            "production_style": [p for p, var in self.prod_vars.items() if var.get()],
            "energy_level":     [e for e, var in self.energy_vars.items() if var.get()],
            "use_case":         [u for u, var in self.usecase_vars.items() if var.get()],
            "comments":         [c.strip() for c in self.comments_entry.get("1.0", "end").strip().split(",") if c.strip() != '']
        }

    def save_state(self):
        try:
            self.controller.app_state.save_to_file("appstate.json")
            print("[TaggingScene] State saved")
        except Exception as e:
            print(f"[TaggingScene] Error saving state: {e}")

    def press_key(self, hexKeyCode):
        ctypes.windll.user32.keybd_event(hexKeyCode, 0, 0, 0) 
        time.sleep(0.05)
        ctypes.windll.user32.keybd_event(hexKeyCode, 0, 2, 0)    

    def save_and_continue(self):
        self.save()
        self.press_key(0xB0)

        self.load_next_track()

    def save_and_exit(self):
        self.save()
        self.controller.quit()

    def save(self):
        self.controller.app_state.tagged_tracks.append(self.collect_data())
        self.controller.app_state.current_track_index += 1
        self.save_state()

    def clear_fields(self):
        self.rating_entry.delete(0, tk.END)
        for var in self.genre_vars.values():
            var.set(False)
        for var in self.tempo_vars.values():
            var.set(False)
        for var in self.tone_vars.values():
            var.set(False)
        for var in self.mood_vars.values():
            var.set(False)
        for var in self.vocals_vars.values():
            var.set(False)
        for var in self.guitar_vars.values():
            var.set(False)
        for var in self.synth_vars.values():
            var.set(False)
        for var in self.prod_vars.values():
            var.set(False)
        for var in self.energy_vars.values():
            var.set(False)
        for var in self.usecase_vars.values():
            var.set(False)
        self.comments_entry.delete("1.0", tk.END)
