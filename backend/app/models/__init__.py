# Import all models to make them available
from app.models.user import User  # noqa: F401
from app.models.movie import Movie  # noqa: F401
from app.models.review import Review  # noqa: F401
from app.models.watchlist import Watchlist  # noqa: F401

__all__ = ["User", "Movie", "Review", "Watchlist"]
