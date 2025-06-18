import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from core import auth, playlist_scrapper


def notfav_artists(session, tracks):
    artists_in_playlist = set()
    for track in tracks:
        artists_in_playlist.add(track.artist.name)

    favorite_artists = session.user.favorites.artists()
    print("Artists not in favorites:")
    for artist in artists_in_playlist:
        if artist not in [fav_artist.name for fav_artist in favorite_artists]:
            print(artist)

def notfav_tracks(session, tracks):
    favorite_tracks = session.user.favorites.tracks()
    favorite_tracks_ids = [fav_track.id for fav_track in favorite_tracks]
    notfav = []
    print("Tracks not in favorites:")
    for track in tracks:
        if track.id not in favorite_tracks_ids:
            print(f"{track.artist.name} - {track.name}")
            notfav.append(track)
    return notfav


session = auth.authorize_tidal()
choose = False

if choose:
    playlists = playlist_scrapper.get_all_playlists(session)
    if not playlists:
        print("No playlists found.")
        exit()
    print("Select a playlist to get tracks from:")
    for i, pl in enumerate(playlists, start=1):
        print(f"{i}. {pl.name} (ID: {pl.id})")
    choice = input("Enter the number of the playlist: ")
    try:
        choice_index = int(choice) - 1
        if 0 <= choice_index < len(playlists):
            selected_playlist = playlists[choice_index]
            print(f"Selected playlist: {selected_playlist.name} (ID: {selected_playlist.id})")
            tracks = playlist_scrapper.get_tracks_from_playlist(session, selected_playlist.id)
        else:
            print("Invalid choice.")
    except ValueError:
        print("Please enter a valid number.")
else:
    tracks = session.user.favorites.tracks()
# menu
print("Select an option:")
print("1. List artists not in favorites")
print("2. List tracks not in favorites")
print("3. List favorite tracks")
print("4. Exit")
option = input("Enter your choice: ")
if option == '1':
    notfav_artists(session, tracks)
elif option == '2':
    notfav = notfav_tracks(session, tracks)
    print("Want to create a playlist with these tracks? (y/n)")
    create_playlist_choice = input().strip().lower()
    if create_playlist_choice == 'y':
        playlist = session.user.create_playlist("not in fav", "")
        playlist.add([track.id for track in notfav])
        print(f"Playlist '{playlist.name}' created with {len(notfav)} tracks.")
elif option == '3':
    fav_tracks = session.user.favorites.tracks()
    fav_tracks_sorted = sorted(fav_tracks, key=lambda track: (track.artist.name.lower(), track.album.name.lower()))
    print("Your favorite tracks:")
    for track in fav_tracks_sorted:
        print(f"{track.artist.name} - {track.name}, (ID: {track.id})")
    print("Total favorite tracks:", len(fav_tracks_sorted))
elif option == '4':
    print("Exiting...")
    exit()
