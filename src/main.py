from core import auth, playlistScrapper

session = auth.authorize_tidal()
scrappedTracks = playlistScrapper.choose_playlist_and_print_tracks(session)
