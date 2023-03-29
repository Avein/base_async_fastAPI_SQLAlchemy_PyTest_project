from typing import List

from httpx import AsyncClient

from app.api.artists.schemas import ImportArtistSchema
from app.envs import Env


async def get_access_token(client: AsyncClient) -> str:

    auth_response = await client.post(
        f"{Env.client.spotify.SPOTIFY_BASE_URL}/api/token",
        auth=(
            Env.client.spotify.SPOTIFY_CLIENT_ID,
            Env.client.spotify.SPOTIFY_CLIENT_SECRET
        ),
        data={"grant_type": "client_credentials"},
        )
    auth_data = auth_response.json()
    access_token = auth_data["access_token"]

    return access_token


async def get_artists_by_playlist(
        client: AsyncClient, access_token: str, playlist_id: str
) -> List[str]:

    response = await client.get(
        f"https://api.spotify.com/v1/playlists/{playlist_id}/tracks",
        headers={"Authorization": f"Bearer {access_token}"},
        params={"limit": 50}
    )

    artist_ids = list()
    songs = response.json()

    for song in songs['items']:
        artists = song['track']['artists']
        for artist_id in artists:
            artist_ids.append(artist_id['id'])

    return artist_ids


async def get_artists(
        client: AsyncClient, access_token: str
) -> List[ImportArtistSchema]:

    artists_ids = await get_artists_by_playlist(
        client, access_token, Env.client.spotify.SPOTIFY_DEFAULT_PLAYLIST_ID
    )

    response = await client.get(
        f"https://api.spotify.com/v1/artists",

        headers={"Authorization": f"Bearer {access_token}"},
        params={
            "limit": 50,
            "ids": ','.join(artists_ids[:50])
        }
    )
    return [ImportArtistSchema.parse_obj(x) for x in response.json()['artists']]
