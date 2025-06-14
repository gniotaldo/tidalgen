import tidalapi

def get_all_playlists(session: tidalapi.Session):
    return list(session.user.playlists())

def get_tracks_from_playlist(session: tidalapi.Session, playlist_id: str):
    playlist = tidalapi.Playlist(session, playlist_id)
    return list(playlist.tracks())

def get_liked_tracks(session: tidalapi.Session):
    return list(session.user.favorites.tracks())

def choose_playlist_and_print_tracks(session: tidalapi.Session):
    playlists = get_all_playlists(session)
    liked_tracks = get_liked_tracks(session)

    if not playlists and not liked_tracks:
        print("[Playlist Scrapper] No playlists or liked tracks available.")
        return

    print("[Playlist Scrapper] Your playlists:")
    for i, pl in enumerate(playlists, start=1):
        print(f"{i}. {pl.name} (id: {pl.id})")

    liked_option_index = len(playlists) + 1
    print(f"{liked_option_index}. Liked Tracks")

    while True:
        choice = input(f"Choose a playlist number (1-{liked_option_index}): ")
        if not choice.isdigit():
            print("[Playlist Scrapper] Please enter a number.")
            continue
        idx = int(choice)
        if 1 <= idx <= liked_option_index:
            break
        else:
            print("[Playlist Scrapper] Invalid number, please try again.")

    if idx == liked_option_index:
        print("\nYour liked tracks:")
        tracks = liked_tracks
    else:
        selected_playlist = playlists[idx - 1]
        print(f"\nTracks from playlist '{selected_playlist.name}':")
        tracks = get_tracks_from_playlist(session, selected_playlist.id)

    for track in tracks:
        print(f"{track.artist.name} - {track.name}")
    return tracks