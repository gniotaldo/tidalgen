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
        
        canvas = tk.Canvas(self)
        scrollbar = ttk.Scrollbar(self, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas)
        
        self.canvas = canvas
        self.scrollable_frame = scrollable_frame
        self.canvas_window = None
        
        def configure_scroll_region(event=None):
            canvas.update_idletasks()
            bbox = canvas.bbox("all")
            canvas_height = canvas.winfo_height()
            
            if bbox and canvas_height > 1:
                content_height = bbox[3] - bbox[1]
                if content_height <= canvas_height:
                    canvas.configure(scrollregion=(0, 0, 0, 0))
                    canvas.unbind_all("<MouseWheel>")
                    return
                else:
                    canvas.bind_all("<MouseWheel>", _on_mousewheel)
            
            canvas.configure(scrollregion=bbox)
            canvas.after_idle(center_content)
        
        def center_content():
            canvas.update_idletasks()
            canvas_width = canvas.winfo_width()
            frame_width = scrollable_frame.winfo_reqwidth()
            
            if canvas_width > 1:
                x_position = max(0, (canvas_width - frame_width) // 2)
                if self.canvas_window:
                    canvas.coords(self.canvas_window, x_position, 0)
        
        self.canvas_window = canvas.create_window(0, 0, window=scrollable_frame, anchor="n")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        scrollable_frame.bind("<Configure>", configure_scroll_region)
        canvas.bind("<Configure>", lambda e: canvas.after_idle(center_content))
        
        self.bind("<Map>", lambda e: canvas.after_idle(center_content))
        canvas.bind("<Visibility>", lambda e: canvas.after_idle(center_content))
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        def _on_mousewheel(event):
            canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        canvas.bind_all("<MouseWheel>", _on_mousewheel)
    
        self.after(100, center_content)
        
        # LAYOUT
        # TOP CENTER
        # Image
        self.image_label = tk.Label(scrollable_frame)
        self.image_label.pack(pady=5)

        # Track
        self.title_label = tk.Label(scrollable_frame, font=("Arial", 16, "bold"))
        self.title_label.pack()

        # Album
        self.album_label = tk.Label(scrollable_frame, font=("Arial", 12))
        self.album_label.pack(pady=5)

        # MAIN CONTAINER
        main_container = tk.Frame(scrollable_frame)
        main_container.pack(fill='both', expand=True, padx=10, pady=10)

        left_column = tk.Frame(main_container)
        left_column.grid(row=0, column=0, sticky='nsew', padx=5)
        
        middle_column = tk.Frame(main_container)
        middle_column.grid(row=0, column=1, sticky='nsew', padx=5)
        
        right_column = tk.Frame(main_container)
        right_column.grid(row=0, column=2, sticky='nsew', padx=5)

        main_container.grid_columnconfigure(0, weight=1)
        main_container.grid_columnconfigure(1, weight=1)
        main_container.grid_columnconfigure(2, weight=1)

        def create_checkboxes(parent, label, options, var_dict, max_per_row=2):
            tk.Label(parent, text=label, width=20, anchor='w').pack(pady=(8, 0))
            
            frame_outer = tk.Frame(parent)
            frame_outer.pack(fill='x', padx=5)
            frame_inner = tk.Frame(frame_outer)
            frame_inner.pack()
            frame_inner.config(width=280)
            frame_inner.pack_propagate(False)

            for i, opt in enumerate(options):
                var = tk.BooleanVar()
                cb = tk.Checkbutton(frame_inner, text=opt, variable=var, width=15, anchor='w')
                row = i // max_per_row
                col = i % max_per_row
                cb.grid(row=row, column=col, padx=2, pady=2, sticky='w')
                var_dict[opt] = var

            for col in range(max_per_row):
                frame_inner.grid_columnconfigure(col, weight=1, minsize=130, uniform="checkbox_uniform")

        # LEFT COLUMN
        rating_label = tk.Label(left_column, text="Rating (0-10):", width=20, anchor='w')
        rating_label.pack(pady=(10,0))
        self.rating_entry = tk.Entry(left_column, width=35)
        self.rating_entry.pack(padx=(5, 60), pady=2)

        self.genre_vars = {}
        create_checkboxes(left_column, "Genres:", self.GENRES, self.genre_vars)

        self.tempo_vars = {}
        create_checkboxes(left_column, "Tempo:", self.TEMPOS, self.tempo_vars)

        self.tone_vars = {}
        create_checkboxes(left_column, "Tone:", self.TONES, self.tone_vars)

        # MIDDLE COLUMN
        self.mood_vars = {}
        create_checkboxes(middle_column, "Mood:", self.MOODS, self.mood_vars)

        self.vocals_vars = {}
        create_checkboxes(middle_column, "Vocals:", self.VOCALS, self.vocals_vars)

        self.guitar_vars = {}
        create_checkboxes(middle_column, "Guitar Intensity:", self.GUITAR_INTENSITY, self.guitar_vars)

        self.synth_vars = {}
        create_checkboxes(middle_column, "Synth Presence:", self.SYNTH_PRESENCE, self.synth_vars)

        # RIGHT COLUMN
        self.prod_vars = {}
        create_checkboxes(right_column, "Production Style:", self.PRODUCTION_STYLE, self.prod_vars)

        self.energy_vars = {}
        create_checkboxes(right_column, "Energy Level:", self.ENERGY_LEVEL, self.energy_vars)

        self.usecase_vars = {}
        create_checkboxes(right_column, "Use Case:", self.USE_CASE, self.usecase_vars)

        # BOTTOM SECTION
        # Comments
        comments_frame = tk.Frame(scrollable_frame)
        comments_frame.pack(fill='x', padx=10, pady=5)
        tk.Label(comments_frame, text="Comments:").pack(pady=(8,0))
        self.comments_entry = tk.Text(comments_frame, height=4, width=60)
        self.comments_entry.pack(padx=5, pady=2)

        # Buttons
        btn_frame = tk.Frame(scrollable_frame)
        btn_frame.pack(pady=10)
        tk.Button(btn_frame, text="Save & Continue", command=self.save_and_continue).pack(side="left", padx=10)
        tk.Button(btn_frame, text="Save & Exit", command=self.save_and_exit).pack(side="right", padx=10)

        # Progress
        self.progress_label = tk.Label(scrollable_frame, text="Progress: 0/0")
        self.progress_label.pack(pady=5)
    

    def load_next_track(self):
        self.progress_label.config(text=f"Progress: {self.controller.app_state.current_track_index + 1}/{len(self.controller.app_state.current_playlist.tracks())}")
        state = self.controller.app_state
        if state.current_track_index >= len(state.current_playlist.tracks()):
            messagebox.showinfo("Done", "All tracks tagged!")
            self.controller.app_state.is_tagging = False
            self.controller.show_frame("main_menu")
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
        for var_group in [
            self.genre_vars,
            self.tempo_vars,
            self.tone_vars,
            self.mood_vars,
            self.vocals_vars,
            self.guitar_vars,
            self.synth_vars,
            self.prod_vars,
            self.energy_vars,
            self.usecase_vars
        ]:
            for var in var_group.values():
                var.set(False)
        self.comments_entry.delete("1.0", tk.END)
