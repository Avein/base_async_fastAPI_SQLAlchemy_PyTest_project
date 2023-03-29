from app.api.artists.schemas import CreateArtistSchema, UpdateArtistSchema

artists_fixtures = [
    CreateArtistSchema(name='Foo', popularity=67, spotify_artist_id='dddd'),
    CreateArtistSchema(name='Bar', popularity=67, spotify_artist_id='2222'),
    CreateArtistSchema(name='Baz', popularity=67, spotify_artist_id='3333'),
    CreateArtistSchema(
        name='Roco', popularity=67, spotify_artist_id='4444', imported=True
    ),
]


create_artist_fixture = CreateArtistSchema(
    name='Fifi', popularity=47, spotify_artist_id='sss'
)

update_artist_fixture = UpdateArtistSchema(
    name='Lulu', popularity=87
)