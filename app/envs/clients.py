from pydantic import BaseSettings, Field


class SpotifyEnv(BaseSettings):
    SPOTIFY_BASE_URL: str = Field('https://accounts.spotify.com')
    SPOTIFY_CLIENT_ID: str = Field(description='Spotify Client ID')
    SPOTIFY_CLIENT_SECRET: str = Field(description='Spotify Client Secret')
    SPOTIFY_DEFAULT_PLAYLIST_ID: str = Field(
        default='37i9dQZF1DWU0ScTcjJBdj',
        description='Default playlist id used to fetch artist from this playlist'
    )


class ClientsEnv:
    spotify = SpotifyEnv()
