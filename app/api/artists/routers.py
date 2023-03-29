from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status
from starlette.responses import JSONResponse

from app.api.artists import crud
from app.api.artists.schemas import ReadArtistSchema, CreateArtistSchema, \
    UpdateArtistSchema
from app.db.session import Session

router = APIRouter()


@router.get(
    "/artists/",
    response_model=List[ReadArtistSchema],
    status_code=status.HTTP_200_OK
)
async def read_artists(db: AsyncSession = Depends(Session)):
    response = await crud.get_artists(db, limit=10)
    return response


@router.get(
    "/artists/{artist_id}",
    response_model=ReadArtistSchema,
    status_code=status.HTTP_200_OK
)
async def read_artists(artist_id: int, db: AsyncSession = Depends(Session)):
    artist = await crud.get_artist_by_id(db, artist_id)
    if not artist:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={'Error': 'Artist does not exists'}
        )
    return artist


@router.post(
    "/artists/",
    response_model=ReadArtistSchema,
    status_code=status.HTTP_201_CREATED
)
async def create_artist(
        crete_artist: CreateArtistSchema, db: AsyncSession = Depends(Session)
):
    artist = await crud.get_artist_by_spotify_id(
        db, crete_artist.spotify_artist_id
    )
    if artist:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={'Error': 'Artist already exists'}
        )

    created_artist = await crud.create_artist(db, crete_artist)
    return created_artist


@router.put(
    "/artists/{artist_id}",
    response_model=ReadArtistSchema,
    status_code=status.HTTP_200_OK
)
async def update_artist(
        artist_id: int,
        update_artist: UpdateArtistSchema,
        db: AsyncSession = Depends(Session)
):
    artist = await crud.get_artist_by_id(
        db, artist_id
    )
    if not artist:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={'Error': 'Artist does not exists'}
        )
    if artist.imported is True:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={'Error': 'Cannot update auto-imported artist'}
        )

    updated_artist = await crud.update_artist(
        db, artist, update_artist
    )
    return updated_artist


@router.delete(
    "/artists/{artist_id}",
    status_code=status.HTTP_204_NO_CONTENT
)
async def delete_artist(artist_id: int, db: AsyncSession = Depends(Session)):
    artist = await crud.get_artist_by_id(
        db, artist_id
    )
    if not artist:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={'Error': 'Artist does not exists'}
        )

    await crud.delete_artist(db, artist)
