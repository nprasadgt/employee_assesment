from fastapi import FastAPI, HTTPException, Query, Depends
from pydantic import BaseModel, validator
from typing import List, Optional
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship, Session

app = FastAPI()

DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


class Book(BaseModel):
    title: str
    author: str
    publication_year: int

class Review(BaseModel):
    book_id: int
    text: str
    rating: int
    @validator('rating')
    def rating_val(cls, v):
        if v < 1 or v > 5:
            raise ValueError('Rating must be between 1 and 5')
        return v

books = []
reviews = []


class DBBook(Base):
    __tablename__ = "books"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    author = Column(String, index=True)
    publication_year = Column(Integer)


class DBReview(Base):
    __tablename__ = "reviews"
    id = Column(Integer, primary_key=True, index=True)
    book_id = Column(Integer, ForeignKey('books.id'))
    text = Column(String)
    rating = Column(Integer)
    book = relationship("DBBook")

Base.metadata.create_all(bind=engine)

@app.get("/health_check")
def check():
    return {"details": "health check"}


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/add_book")
def add_book(book: Book, db: Session = Depends(get_db)):
    book_dict = book.dict()
    book_dict['id'] = len(books) + 1
    books.append(book_dict)
    db_book = DBBook(**book.dict())
    db.add(db_book)
    db.commit()
    return book_dict


@app.post("/reviews")
def add_review(review: Review):
    if review.book_id > len(books) or review.book_id < 1:
        raise HTTPException(status_code=404, detail="Book not found")
    review_dict = review.dict()
    reviews.append(review_dict)
    return review_dict


@app.get("/get_book")
def get_books(author: Optional[str] = None, year: Optional[int] = None):
    filtered_books = books
    if author:
        filtered_books = [book for book in filtered_books if book['author'] == author]
    if year:
        filtered_books = [book for book in filtered_books if book['publication_year'] == year]
    return filtered_books


@app.get("/reviews/{book_id}")
def get_reviews_for_book(book_id: int):
    book_reviews = [review for review in reviews if review['book_id'] == book_id]
    if not book_reviews:
        raise HTTPException(status_code=404, detail="No reviews found for this book")
    return book_reviews
