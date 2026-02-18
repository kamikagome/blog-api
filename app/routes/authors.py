"""Author routes"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import Author
from app.schemas import AuthorCreate, AuthorUpdate, Author as AuthorSchema, AuthorDetail

router = APIRouter(prefix="/authors", tags=["authors"])


@router.post("", response_model=AuthorSchema)
def create_author(author: AuthorCreate, db: Session = Depends(get_db)):
    """Create a new author"""
    db_author = db.query(Author).filter(Author.email == author.email).first()
    if db_author:
        raise HTTPException(status_code=400, detail="Email already registered")

    db_author = Author(**author.model_dump())
    db.add(db_author)
    db.commit()
    db.refresh(db_author)
    return db_author


@router.get("/{author_id}", response_model=AuthorDetail)
def get_author(author_id: int, db: Session = Depends(get_db)):
    """Get author by ID with their posts"""
    db_author = db.query(Author).filter(Author.id == author_id).first()
    if not db_author:
        raise HTTPException(status_code=404, detail="Author not found")
    return db_author


@router.put("/{author_id}", response_model=AuthorSchema)
def update_author(author_id: int, author: AuthorUpdate, db: Session = Depends(get_db)):
    """Update author"""
    db_author = db.query(Author).filter(Author.id == author_id).first()
    if not db_author:
        raise HTTPException(status_code=404, detail="Author not found")

    update_data = author.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_author, field, value)

    db.commit()
    db.refresh(db_author)
    return db_author


@router.delete("/{author_id}")
def delete_author(author_id: int, db: Session = Depends(get_db)):
    """Delete author"""
    db_author = db.query(Author).filter(Author.id == author_id).first()
    if not db_author:
        raise HTTPException(status_code=404, detail="Author not found")

    db.delete(db_author)
    db.commit()
    return {"message": "Author deleted"}


@router.get("", response_model=list[AuthorSchema])
def list_authors(db: Session = Depends(get_db)):
    """List all authors"""
    return db.query(Author).all()


@router.get("/{author_id}/posts")
def get_author_posts(author_id: int, db: Session = Depends(get_db)):
    """Get all posts by an author"""
    db_author = db.query(Author).filter(Author.id == author_id).first()
    if not db_author:
        raise HTTPException(status_code=404, detail="Author not found")
    return db_author.posts
