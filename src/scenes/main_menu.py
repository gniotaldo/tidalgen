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
        print("[MainMenuScene] Start tagging - not implemented yet")
        self.controller.show_frame("playlist_lister")
        self.controller.state.is_tagging = True

    def continue_tagging(self):
        print("[MainMenuScene] Continue tagging - not implemented yet")
        # load last tagging progress
        # ...
        self.controller.show_frame("tagging")

    def playlist_generator(self):
        print("[MainMenuScene] Playlist generator - not implemented yet")
