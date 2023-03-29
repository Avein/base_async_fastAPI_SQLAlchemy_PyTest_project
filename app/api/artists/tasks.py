from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.artists import crud
from app.api.artists.schemas import CreateArtistSchema, UpdateArtistSchema
from app.clients.spotify import get_access_token, get_artists


async def fetch_top_artists(db: AsyncSession):
    async with AsyncClient() as client:
        access_token = await get_access_token(client)

        data = await get_artists(client, access_token)
        for artist_data in data:

            artist = await crud.get_artist_by_spotify_id(
                db, artist_data.spotify_artist_id
            )
            if not artist:
                await crud.create_artist(
                    db, CreateArtistSchema(**artist_data.dict())
                )
            else:
                await crud.update_artist(
                    db, artist, UpdateArtistSchema(**artist_data.dict())
                )
