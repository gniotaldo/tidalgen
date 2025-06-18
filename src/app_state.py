import json
from core.playlist_scrapper import get_all_playlists

class AppState:
    def __init__(self):
        self.session = None
        self.user_playlists = []
        self.current_playlist = None
        self.current_track_index = 0
        self.tagged_tracks = []
        self.is_tagging = False

    def save_to_file(self, filepath):
        if not self.current_playlist:
            pl_id = None
        elif hasattr(self.current_playlist, 'id'):
            pl_id = self.current_playlist.id
        else:
            pl_id = -1

        data = {
            "current_playlist_id": pl_id,
            "current_track_index": self.current_track_index,
            "tagged_tracks": self.tagged_tracks,
        }
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)

    def load_from_file(self, filepath):

        with open(filepath, "r", encoding="utf-8") as f:
            data = json.load(f)
        self.user_playlists = get_all_playlists(self.session)
        playlist_id = data.get("current_playlist_id")
        if playlist_id == -1:
            self.current_playlist = self.session.user.favorites
        else:
            self.current_playlist = next((pl for pl in self.user_playlists if pl.id == playlist_id), None)
        print(self.current_playlist)

        self.current_track_index = data.get("current_track_index", 0)
        self.tagged_tracks = data.get("tagged_tracks", [])

state = AppState()
