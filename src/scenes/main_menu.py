import tkinter as tk

class MainMenuScene(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        tk.Label(self, text="Main Menu", font=("Arial", 18)).pack(pady=30)

        buttons = [
            ("Playlists Preview", self.preview_playlists),
            ("Start Tagging", self.start_tagging),
            ("Continue Tagging", self.continue_tagging),
            ("Playlist Generator", self.playlist_generator),
            ("Exit", self.controller.quit)
        ]

        for text, command in buttons:
            tk.Button(self, text=text, font=("Arial", 14), width=25, command=command).pack(pady=10)

    def preview_playlists(self):
        print("[MainMenuScene] Previewing playlists...")
        playlist_scene = self.controller.frames.get("playlist_lister")
        if playlist_scene:
            playlist_scene.load_playlists()

        self.controller.show_frame("playlist_lister")

    def start_tagging(self):
        print("[MainMenuScene] Start tagging...")
        self.controller.app_state.is_tagging = True
        self.controller.app_state.current_track_index = 0
        self.controller.app_state.tagged_tracks = []
        playlist_scene = self.controller.frames.get("playlist_lister")
        if playlist_scene:
            playlist_scene.load_playlists()

        self.controller.show_frame("playlist_lister")

    def continue_tagging(self):
        print("[MainMenuScene] Loading last tagging progress...")
        self.controller.app_state.load_from_file("appstate.json")
        print(self.controller.app_state.current_playlist)
        tagging_scene = self.controller.frames.get("tagging")
        self.controller.app_state.is_tagging = True
        if tagging_scene:
            tagging_scene.load_next_track()
        if self.controller.app_state.is_tagging:
            self.controller.show_frame("tagging")

    def playlist_generator(self):
        print("[MainMenuScene] Playlist generator - not implemented yet")
