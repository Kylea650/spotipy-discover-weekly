import spotipy
from spotipy.oauth2 import SpotifyOAuth
from config import credentials
from datetime import datetime


client = spotipy.Spotify(
    auth_manager=SpotifyOAuth(
        client_id=credentials.CLIENT_ID,
        client_secret=credentials.CLIENT_SECRET,
        redirect_uri=credentials.REDIRECT_URI,
        scope=[
            "playlist-read-private",
            "playlist-modify-private",
        ],
    )
)


def get_discover_weekly_tracks(playlist_id) -> list[str]:
    """
    returns all track URIs for the current week's Discover Weekly playlist
    """
    discover_weekly_tracks = client.playlist_tracks(playlist_id=playlist_id)
    return [track["track"]["uri"] for track in discover_weekly_tracks["items"]]


def get_discover_weekly_date(playlist_id) -> str:
    """
    returns the playlist date of the current week's Discover Weekly playlist
    in YYYY-MM-DD format
    """
    playlist = client.playlist(playlist_id=playlist_id)
    created_date = datetime.strptime(
        playlist["tracks"]["items"][0]["added_at"], "%Y-%m-%dT%H:%M:%S%z"
    )
    return created_date.strftime("%Y-%m-%d")


def create_new_playlist(playlist_id) -> dict:
    """
    creates a new Spotify playlist for the current Discover Weekly playlist
    to be archived and returns the new playlist info as a dict object
    """
    user = credentials.USER_ID
    date = get_discover_weekly_date(playlist_id=playlist_id)
    new_playlist = client.user_playlist_create(
        user=user,
        name=f"Discover(ed) Weekly {date}",
        public=False,
        description=f"Archived Discover Weekly playlist for week of {date}",
    )
    return new_playlist


def archive_discover_weekly(playlist_id, new_playlist) -> None:
    """
    adds tracks from current Discover Weekly playlist into
    newly created archived Discover(ed) Weekly playlist
    """
    user = credentials.USER_ID
    client.user_playlist_add_tracks(
        user=user,
        playlist_id=new_playlist["id"],
        tracks=get_discover_weekly_tracks(playlist_id=playlist_id),
    )


def main():
    playlist_id = credentials.PLAYLIST_ID
    new_playlist = create_new_playlist(playlist_id=playlist_id)
    archive_discover_weekly(playlist_id=playlist_id, new_playlist=new_playlist)


if __name__ == "__main__":
    main()
