import logging
import os
import sys
from datetime import datetime

import spotipy
from spotipy import SpotifyOauthError
from spotipy.oauth2 import SpotifyOAuth

logger = logging.getLogger("discovered-weekly")
handler = logging.StreamHandler()
handler.setFormatter(logging.Formatter(fmt="%(asctime)s : %(levelname)s : %(message)s"))
logger.setLevel(logging.INFO)
logger.addHandler(handler)


try:  # for running locally
    from config import credentials

    CLIENT_ID = credentials.CLIENT_ID
    CLIENT_SECRET = credentials.CLIENT_SECRET
    REDIRECT_URI = credentials.REDIRECT_URI
    USER_ID = credentials.USER_ID
    PLAYLIST_ID = credentials.PLAYLIST_ID
    REFRESH_TOKEN = credentials.REFRESH_TOKEN

except:  # for running with GitHub Actions
    CLIENT_ID = os.environ["CLIENT_ID"]
    CLIENT_SECRET = os.environ["CLIENT_SECRET"]
    REDIRECT_URI = os.environ["REDIRECT_URI"]
    USER_ID = os.environ["USER_ID"]
    PLAYLIST_ID = os.environ["PLAYLIST_ID"]
    REFRESH_TOKEN = os.environ["REFRESH_TOKEN"]


def get_client(client_id, client_secret, redirect_uri, user, refresh_token):
    """
    returns the authenticated Spotify client
    """
    auth_manager = SpotifyOAuth(
        client_id=client_id,
        client_secret=client_secret,
        redirect_uri=redirect_uri,
        scope=[
            "playlist-read-private",
            "playlist-modify-private",
            "playlist-read-collaborative"
        ],
        username=user
    )
    auth_manager.refresh_access_token(refresh_token)
    client = spotipy.Spotify(auth_manager=auth_manager)
    return client


def get_discover_weekly_tracks(client, playlist_id) -> list[str]:
    """
    returns all track URIs for the current week's Discover Weekly playlist
    """
    logger.info("Retrieving tracks from this week's Discovered Weekly")

    discover_weekly_tracks = client.playlist_tracks(playlist_id=playlist_id)
    return [track["track"]["uri"] for track in discover_weekly_tracks["items"]]


def get_discover_weekly_date(client, playlist_id) -> str:
    """
    returns the playlist date of the current week's Discover Weekly playlist
    in YYYY-MM-DD format
    """
    playlist = client.playlist_items(playlist_id=playlist_id)
    created_date = datetime.strptime(
        playlist["items"][0]["added_at"], "%Y-%m-%dT%H:%M:%S%z"
    )
    return created_date.strftime("%Y-%m-%d")


def create_new_playlist(client, user, playlist_id) -> dict:
    """
    creates a new Spotify playlist for the current Discover Weekly playlist
    to be archived and returns the new playlist info as a dict object
    """
    logger.info("Creating a new empty playlist")

    date = get_discover_weekly_date(client=client, playlist_id=playlist_id)
    new_playlist = client.user_playlist_create(
        user=user,
        name=f"Discover(ed) Weekly {date}",
        public=False,
        description=f"Archived Discover Weekly playlist for week of {date}",
    )
    return new_playlist


def archive_discover_weekly(client, user, playlist_id, new_playlist) -> None:
    """
    adds tracks from current Discover Weekly playlist into
    newly created archived Discover(ed) Weekly playlist
    """
    client.user_playlist_add_tracks(
        user=user,
        playlist_id=new_playlist["id"],
        tracks=get_discover_weekly_tracks(client=client, playlist_id=playlist_id),
    )


def main() -> None:
    
    logger.info(f"Beginning Discovered Weekly archive")

    user = USER_ID
    playlist_id = PLAYLIST_ID

    logger.info("Connecting to Spotify with provided client credentials")
    try:
        client = get_client(
            client_id=CLIENT_ID,
            client_secret=CLIENT_SECRET,
            redirect_uri=REDIRECT_URI,
            user=user,
            refresh_token=REFRESH_TOKEN,
        )
    except SpotifyOauthError:
        logger.error("Invalid client credentials provided")
        sys.exit(1)

    new_playlist = create_new_playlist(
        client=client, user=user, playlist_id=playlist_id
    )

    archive_discover_weekly(
        client=client, user=user, playlist_id=playlist_id, new_playlist=new_playlist
    )

    logger.info("Discovered Weekly archiving complete")


if __name__ == "__main__":
    main()
