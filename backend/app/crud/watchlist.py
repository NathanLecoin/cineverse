from sqlalchemy.orm import Session, joinedload
from app.models.watchlist import Watchlist
from app.schemas.watchlist import WatchlistCreate

def add_to_watchlist(db: Session, watchlist: WatchlistCreate):
    # Vérifier si déjà dans la watchlist
    existing = db.query(Watchlist).filter(
        Watchlist.user_id == watchlist.user_id,
        Watchlist.movie_id == watchlist.movie_id
    ).first()
    
    if existing:
        return existing
    
    db_watchlist = Watchlist(**watchlist.model_dump())
    db.add(db_watchlist)
    db.commit()
    db.refresh(db_watchlist)
    return db_watchlist

def get_watchlist(db: Session, watchlist_id: int):
    return db.query(Watchlist).filter(Watchlist.id == watchlist_id).first()

def get_user_watchlist(db: Session, user_id: int):
    return db.query(Watchlist)\
        .options(joinedload(Watchlist.movie))\
        .filter(Watchlist.user_id == user_id)\
        .all()

def remove_from_watchlist(db: Session, user_id: int, movie_id: int):
    db_watchlist = db.query(Watchlist).filter(
        Watchlist.user_id == user_id,
        Watchlist.movie_id == movie_id
    ).first()
    
    if db_watchlist:
        db.delete(db_watchlist)
        db.commit()
    
    return db_watchlist

def is_in_watchlist(db: Session, user_id: int, movie_id: int):
    return db.query(Watchlist).filter(
        Watchlist.user_id == user_id,
        Watchlist.movie_id == movie_id
    ).first() is not None