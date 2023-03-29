from typing import List, Optional

from sqlalchemy.ext.asyncio import AsyncSession

from app.api.artists.schemas import CreateArtistSchema, UpdateArtistSchema
from app.db import models
from sqlalchemy import select


async def get_artists(
        db: AsyncSession, skip: int = 0, limit: int = 10
) -> List[models.Artists]:

    result = await db.execute(select(models.Artists).offset(skip).limit(limit))
    return result.scalars().all()


async def get_artist_by_id(
        db: AsyncSession, artist_id: int
) -> Optional[models.Artists]:

    result = await db.execute(
        select(models.Artists).filter(models.Artists.id == artist_id)
    )
    return result.scalar()


async def get_artist_by_spotify_id(
        db: AsyncSession, spotify_id: str
) -> Optional[models.Artists]:

    result = await db.execute(
        select(models.Artists).filter(
            models.Artists.spotify_artist_id == spotify_id
        )
    )
    return result.scalar()


async def create_artist(
        db: AsyncSession, artist: CreateArtistSchema
) -> models.Artists:

    artist = models.Artists.from_schema(artist)
    await artist.save(db, commit=True)

    return artist


async def update_artist(
        db: AsyncSession, artist: models.Artists, update_data: UpdateArtistSchema
) -> models.Artists:

    for field, values in update_data.dict(exclude_unset=True).items():
        setattr(artist, field, values)

    await artist.save(db, commit=True)
    return artist


async def delete_artist(db: AsyncSession, artist: models.Artists) -> None:
    await artist.remove(db, commit=True)
