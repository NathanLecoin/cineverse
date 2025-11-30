from sqlalchemy.orm import Session
from app.models.review import Review
from app.schemas.review import ReviewCreate, ReviewUpdate

def create_review(db: Session, review: ReviewCreate):
    db_review = Review(**review.model_dump())
    db.add(db_review)
    db.commit()
    db.refresh(db_review)
    return db_review

def get_review(db: Session, review_id: int):
    return db.query(Review).filter(Review.id == review_id).first()

def get_reviews(db: Session, skip: int = 0, limit: int = 10):
    return db.query(Review).offset(skip).limit(limit).all()

def get_reviews_by_movie(db: Session, movie_id: int, skip: int = 0, limit: int = 10):
    return db.query(Review).filter(Review.movie_id == movie_id).offset(skip).limit(limit).all()

def get_reviews_by_user(db: Session, user_id: int, skip: int = 0, limit: int = 10):
    return db.query(Review).filter(Review.user_id == user_id).offset(skip).limit(limit).all()

def update_review(db: Session, review_id: int, review: ReviewUpdate):
    db_review = db.query(Review).filter(Review.id == review_id).first()
    if db_review:
        if review.rating is not None:
            db_review.rating = review.rating
        if review.comment:
            db_review.comment = review.comment
        db.add(db_review)
        db.commit()
        db.refresh(db_review)
    return db_review

def delete_review(db: Session, review_id: int):
    db_review = db.query(Review).filter(Review.id == review_id).first()
    if db_review:
        db.delete(db_review)
        db.commit()
    return db_review