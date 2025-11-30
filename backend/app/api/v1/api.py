from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import Annotated
from app.db.session import get_db
from app.crud.movie import create_movie, get_movie, get_movies, update_movie, delete_movie
from app.crud.review import create_review, get_review, get_reviews, get_reviews_by_movie, get_reviews_by_user, update_review, delete_review
from app.crud.watchlist import add_to_watchlist, get_user_watchlist, remove_from_watchlist, is_in_watchlist
from app.crud.user import create_user, get_user, get_user_by_username, get_user_by_email, get_users, update_user, delete_user
from app.schemas.movie import MovieCreate, MovieUpdate, MovieResponse
from app.schemas.review import ReviewCreate, ReviewUpdate, ReviewResponse
from app.schemas.watchlist import WatchlistCreate, WatchlistResponse
from app.schemas.user import UserCreate, UserUpdate, UserResponse
from app.api.v1 import auth
from app.api.v1.auth import get_current_user, get_current_active_admin
from app.models.user import User

api_router = APIRouter()

# ============ AUTHENTICATION ENDPOINTS ============
api_router.include_router(auth.router, prefix="/auth", tags=["Authentication"])

@api_router.get("/test")
async def test_endpoint():
    """Test endpoint to verify API is working"""
    return {"message": "CineVerse API is working!", "status": "success"}

# ============ USER ENDPOINTS ============

@api_router.post("/users", response_model=UserResponse)
async def create_new_user(user: UserCreate, db: Session = Depends(get_db)):
    """Create a new user"""
    # Vérifier si l'utilisateur existe déjà
    existing_user = get_user_by_username(db, user.username)
    if existing_user:
        raise HTTPException(status_code=400, detail="Username already exists")
    
    existing_email = get_user_by_email(db, user.email)
    if existing_email:
        raise HTTPException(status_code=400, detail="Email already exists")
    
    return create_user(db, user)

@api_router.get("/users", response_model=list[UserResponse])
async def list_users(
    current_admin: Annotated[User, Depends(get_current_active_admin)],
    skip: int = 0,
    limit: int = 10,
    db: Session = Depends(get_db)
):
    """Get all users with pagination (Admin only)"""
    return get_users(db, skip=skip, limit=limit)

@api_router.get("/users/{user_id}", response_model=UserResponse)
async def get_user_by_id(user_id: int, db: Session = Depends(get_db)):
    """Get a specific user by ID"""
    db_user = get_user(db, user_id)
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user

@api_router.get("/users/username/{username}", response_model=UserResponse)
async def get_user_by_username_endpoint(username: str, db: Session = Depends(get_db)):
    """Get a user by username"""
    db_user = get_user_by_username(db, username)
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user

@api_router.put("/users/{user_id}", response_model=UserResponse)
async def update_existing_user(
    user_id: int,
    user: UserUpdate,
    current_user: Annotated[User, Depends(get_current_user)],
    db: Session = Depends(get_db)
):
    """Update an existing user (Owner or Admin only)"""
    # Vérifier que l'utilisateur modifie son propre profil ou est admin
    if current_user.id != user_id and not current_user.is_admin:
        raise HTTPException(status_code=403, detail="Not authorized to update this user")
    
    db_user = update_user(db, user_id, user)
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user

@api_router.delete("/users/{user_id}", response_model=UserResponse)
async def delete_existing_user(
    user_id: int,
    current_user: Annotated[User, Depends(get_current_user)],
    db: Session = Depends(get_db)
):
    """Delete a user (Owner or Admin only)"""
    # Vérifier que l'utilisateur supprime son propre compte ou est admin
    if current_user.id != user_id and not current_user.is_admin:
        raise HTTPException(status_code=403, detail="Not authorized to delete this user")
    
    db_user = delete_user(db, user_id)
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user

# ============ MOVIE ENDPOINTS ============

@api_router.post("/movies", response_model=MovieResponse)
async def create_new_movie(
    movie: MovieCreate,
    current_admin: Annotated[User, Depends(get_current_active_admin)],
    db: Session = Depends(get_db)
):
    """Create a new movie (Admin only)"""
    return create_movie(db, movie)

@api_router.get("/movies", response_model=list[MovieResponse])
async def list_movies(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    """Get all movies with pagination"""
    return get_movies(db, skip=skip, limit=limit)

@api_router.get("/movies/{movie_id}", response_model=MovieResponse)
async def get_movie_by_id(movie_id: int, db: Session = Depends(get_db)):
    """Get a specific movie by ID"""
    db_movie = get_movie(db, movie_id)
    if not db_movie:
        raise HTTPException(status_code=404, detail="Movie not found")
    return db_movie

@api_router.put("/movies/{movie_id}", response_model=MovieResponse)
async def update_existing_movie(
    movie_id: int,
    movie: MovieUpdate,
    current_admin: Annotated[User, Depends(get_current_active_admin)],
    db: Session = Depends(get_db)
):
    """Update an existing movie (Admin only)"""
    db_movie = update_movie(db, movie_id, movie)
    if not db_movie:
        raise HTTPException(status_code=404, detail="Movie not found")
    return db_movie

@api_router.delete("/movies/{movie_id}", response_model=MovieResponse)
async def delete_existing_movie(
    movie_id: int,
    current_admin: Annotated[User, Depends(get_current_active_admin)],
    db: Session = Depends(get_db)
):
    """Delete a movie (Admin only)"""
    db_movie = delete_movie(db, movie_id)
    if not db_movie:
        raise HTTPException(status_code=404, detail="Movie not found")
    return db_movie

# ============ REVIEW ENDPOINTS ============

@api_router.post("/reviews", response_model=ReviewResponse)
async def create_new_review(
    review: ReviewCreate,
    current_user: Annotated[User, Depends(get_current_user)],
    db: Session = Depends(get_db)
):
    """Create a new review (Authenticated users only)"""
    # Vérifier que l'utilisateur crée une review pour lui-même
    if review.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="You can only create reviews for yourself")
    return create_review(db, review)

@api_router.get("/reviews", response_model=list[ReviewResponse])
async def list_reviews(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    """Get all reviews with pagination"""
    return get_reviews(db, skip=skip, limit=limit)

@api_router.get("/reviews/{review_id}", response_model=ReviewResponse)
async def get_review_by_id(review_id: int, db: Session = Depends(get_db)):
    """Get a specific review by ID"""
    db_review = get_review(db, review_id)
    if not db_review:
        raise HTTPException(status_code=404, detail="Review not found")
    return db_review

@api_router.get("/movies/{movie_id}/reviews", response_model=list[ReviewResponse])
async def get_movie_reviews(movie_id: int, skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    """Get all reviews for a specific movie"""
    return get_reviews_by_movie(db, movie_id, skip=skip, limit=limit)

@api_router.get("/users/{user_id}/reviews", response_model=list[ReviewResponse])
async def get_user_reviews(user_id: int, skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    """Get all reviews by a specific user"""
    return get_reviews_by_user(db, user_id, skip=skip, limit=limit)

@api_router.put("/reviews/{review_id}", response_model=ReviewResponse)
async def update_existing_review(
    review_id: int,
    review: ReviewUpdate,
    current_user: Annotated[User, Depends(get_current_user)],
    db: Session = Depends(get_db)
):
    """Update an existing review (Owner or Admin only)"""
    # Vérifier que la review existe
    db_review = get_review(db, review_id)
    if not db_review:
        raise HTTPException(status_code=404, detail="Review not found")
    
    # Vérifier que l'utilisateur modifie sa propre review ou est admin
    if db_review.user_id != current_user.id and not current_user.is_admin:
        raise HTTPException(status_code=403, detail="Not authorized to update this review")
    
    return update_review(db, review_id, review)

@api_router.delete("/reviews/{review_id}", response_model=ReviewResponse)
async def delete_existing_review(
    review_id: int,
    current_user: Annotated[User, Depends(get_current_user)],
    db: Session = Depends(get_db)
):
    """Delete a review (Owner or Admin only)"""
    # Vérifier que la review existe
    db_review = get_review(db, review_id)
    if not db_review:
        raise HTTPException(status_code=404, detail="Review not found")
    
    # Vérifier que l'utilisateur supprime sa propre review ou est admin
    if db_review.user_id != current_user.id and not current_user.is_admin:
        raise HTTPException(status_code=403, detail="Not authorized to delete this review")
    
    return delete_review(db, review_id)

# ============ WATCHLIST ENDPOINTS ============

@api_router.post("/watchlist", response_model=WatchlistResponse)
async def add_movie_to_watchlist(
    watchlist: WatchlistCreate,
    current_user: Annotated[User, Depends(get_current_user)],
    db: Session = Depends(get_db)
):
    """Add a movie to watchlist (Owner only)"""
    # Vérifier que l'utilisateur ajoute à sa propre watchlist
    if watchlist.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="You can only add movies to your own watchlist")
    return add_to_watchlist(db, watchlist)

@api_router.get("/watchlist/{user_id}", response_model=list[WatchlistResponse])
async def get_watchlist(
    user_id: int,
    current_user: Annotated[User, Depends(get_current_user)],
    db: Session = Depends(get_db)
):
    """Get user's watchlist (Owner or Admin only)"""
    # Vérifier que l'utilisateur accède à sa propre watchlist ou est admin
    if current_user.id != user_id and not current_user.is_admin:
        raise HTTPException(status_code=403, detail="Not authorized to view this watchlist")
    return get_user_watchlist(db, user_id)

@api_router.delete("/watchlist/{user_id}/{movie_id}", response_model=WatchlistResponse)
async def remove_movie_from_watchlist(
    user_id: int,
    movie_id: int,
    current_user: Annotated[User, Depends(get_current_user)],
    db: Session = Depends(get_db)
):
    """Remove a movie from user's watchlist (Owner only)"""
    # Vérifier que l'utilisateur modifie sa propre watchlist
    if current_user.id != user_id:
        raise HTTPException(status_code=403, detail="You can only remove movies from your own watchlist")
    
    db_watchlist = remove_from_watchlist(db, user_id, movie_id)
    if not db_watchlist:
        raise HTTPException(status_code=404, detail="Movie not in watchlist")
    return db_watchlist

@api_router.get("/watchlist/{user_id}/{movie_id}")
async def check_in_watchlist(user_id: int, movie_id: int, db: Session = Depends(get_db)):
    """Check if a movie is in user's watchlist"""
    in_watchlist = is_in_watchlist(db, user_id, movie_id)
    return {"in_watchlist": in_watchlist}