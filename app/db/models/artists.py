from sqlalchemy import Column, Integer, String, Boolean

from app.db.db import Base


class Artists(Base):
    __tablename__ = "artists"

    spotify_artist_id = Column(String, unique=True, index=True)
    popularity = Column(Integer)
    name = Column(String)
    imported = Column(Boolean, default=False)

