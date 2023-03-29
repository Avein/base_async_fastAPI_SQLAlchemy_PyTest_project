from pydantic import BaseModel, Field


# Request Schemas
class CreateArtistSchema(BaseModel):
    name: str
    popularity: int
    spotify_artist_id: str
    imported: bool = False


class ImportArtistSchema(CreateArtistSchema):
    spotify_artist_id: str = Field(..., alias='id')
    imported: bool = True

    class Config:
        allow_population_by_field_name = True


class UpdateArtistSchema(BaseModel):
    name: str
    popularity: int


# Response Schemas
class ReadArtistSchema(BaseModel):
    id: int
    name: str
    popularity: int
    spotify_artist_id: str

    class Config:
        orm_mode = True


