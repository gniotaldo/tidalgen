class AppState:
    def __init__(self):
        self.session = None
        self.user_playlists = []
        self.current_playlist = None
        self.current_track_index = 0
        self.tagged_tracks = []
        self.is_tagging = False

state = AppState()