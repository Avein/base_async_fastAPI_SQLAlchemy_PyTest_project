import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from app.api.artists import crud
from app.db.session import TestSession
from app.tests.fixtures import artists_fixtures, create_artist_fixture, \
    update_artist_fixture

from app.tests.conftest import async_client, seed_db, session, event_loop  # noqa: F401


@pytest.mark.asyncio
class TestArtists:

    async def test_get_artists(self, async_client: AsyncClient):

        response = await async_client.get(
            "http://0.0.0.0:8000/artists"
        )

        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert len(data) == 4

        for resp_artist, fixture_artist in zip(data, artists_fixtures):
            assert resp_artist['name'] == fixture_artist.name
            assert resp_artist['popularity'] == fixture_artist.popularity
            assert resp_artist['spotify_artist_id'] == \
                   fixture_artist.spotify_artist_id

    async def test_get_artist(self, async_client: AsyncClient):

        response = await async_client.get(
            "http://0.0.0.0:8000/artists/1"
        )

        assert response.status_code == status.HTTP_200_OK
        resp_artist = response.json()

        assert resp_artist['name'] == artists_fixtures[0].name
        assert resp_artist['popularity'] == artists_fixtures[0].popularity
        assert resp_artist['spotify_artist_id'] == \
               artists_fixtures[0].spotify_artist_id

        response = await async_client.get(
            "http://0.0.0.0:8000/artists/10"
        )

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.json() == {'Error': 'Artist does not exists'}

    async def test_create_artist(
            self, async_client: AsyncClient, session: AsyncSession
    ):
        response = await async_client.post(
            "http://0.0.0.0:8000/artists",
            json=create_artist_fixture.dict(),
        )

        assert response.status_code == status.HTTP_201_CREATED
        resp_artist = response.json()

        created_artist = await crud.get_artist_by_id(session, resp_artist['id'])

        assert create_artist_fixture.name == created_artist.name
        assert create_artist_fixture.popularity == created_artist.popularity
        assert create_artist_fixture.spotify_artist_id == \
               created_artist.spotify_artist_id

        response = await async_client.post(
            "http://0.0.0.0:8000/artists",
            json=create_artist_fixture.dict(),
        )

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.json() == {'Error': 'Artist already exists'}

    async def test_update_artist_does_not_exist(
            self, async_client: AsyncClient
    ):
        response = await async_client.put(
            "http://0.0.0.0:8000/artists/10",
            json=create_artist_fixture.dict(),
        )

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.json() == {'Error': 'Artist does not exists'}

    async def test_update_imported_artist(
            self, async_client: AsyncClient, session: AsyncSession
    ):
        imported_artist_to_update = await crud.get_artist_by_id(
            session, 4
        )

        assert imported_artist_to_update.imported is True

        response = await async_client.put(
            f"http://0.0.0.0:8000/artists/{imported_artist_to_update.id}",
            json=create_artist_fixture.dict(),
        )

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.json() == {
            'Error': 'Cannot update auto-imported artist'
        }

    async def test_update_artist(
            self, async_client: AsyncClient, session: AsyncSession
    ):
        artist_to_update = await crud.get_artist_by_id(
            session, 3
        )
        assert artist_to_update.imported is False
        assert artist_to_update.name == artists_fixtures[2].name
        assert artist_to_update.popularity == artists_fixtures[2].popularity
        assert artist_to_update.spotify_artist_id == \
               artists_fixtures[2].spotify_artist_id

        response = await async_client.put(
            f"http://0.0.0.0:8000/artists/{artist_to_update.id}",
            json=update_artist_fixture.dict(),
        )

        assert response.status_code == status.HTTP_200_OK

        async with TestSession.session() as new_session:
            updated_artist = await crud.get_artist_by_id(
                new_session, 3
            )

            assert updated_artist.name == update_artist_fixture.name
            assert updated_artist.popularity == update_artist_fixture.popularity

    async def test_delete_artist(
            self, async_client: AsyncClient, session: AsyncSession
    ):
        artist_to_delete = await crud.get_artist_by_id(session, 2)

        response = await async_client.delete(
            f"http://0.0.0.0:8000/artists/{artist_to_delete.id}",
        )
        assert response.status_code == status.HTTP_204_NO_CONTENT

        async with TestSession.session() as new_session:
            deleted_artist = await crud.get_artist_by_id(
                new_session, 2
            )
        assert deleted_artist is None
