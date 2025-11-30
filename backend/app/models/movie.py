from sqlalchemy import Column, Integer, String, Text
from sqlalchemy.orm import relationship
from app.db.base import Base

class Movie(Base):
    __tablename__ = "movies"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(Text)
    release_year = Column(Integer)

    # Relationships
    reviews = relationship("Review", back_populates="movie")
    watchlists = relationship("Watchlist", back_populates="movie")
