"""Comment routes"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import Comment, Post
from app.schemas import CommentCreate, Comment as CommentSchema, CommentBase

router = APIRouter(prefix="/comments", tags=["comments"])


@router.post("", response_model=CommentSchema)
def create_comment(comment: CommentCreate, db: Session = Depends(get_db)):
    """Create a new comment"""
    post = db.query(Post).filter(Post.id == comment.post_id).first()
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")

    db_comment = Comment(**comment.model_dump())
    db.add(db_comment)
    db.commit()
    db.refresh(db_comment)
    return db_comment


@router.get("/{comment_id}", response_model=CommentSchema)
def get_comment(comment_id: int, db: Session = Depends(get_db)):
    """Get comment by ID"""
    db_comment = db.query(Comment).filter(Comment.id == comment_id).first()
    if not db_comment:
        raise HTTPException(status_code=404, detail="Comment not found")
    return db_comment


@router.put("/{comment_id}", response_model=CommentSchema)
def update_comment(comment_id: int, comment: CommentBase, db: Session = Depends(get_db)):
    """Update comment."""
    db_comment = db.query(Comment).filter(Comment.id == comment_id).first()
    if not db_comment:
        raise HTTPException(status_code=404, detail="Comment not found")

    db_comment.author_name = comment.author_name  # type: ignore
    db_comment.content = comment.content  # type: ignore
    db.commit()
    db.refresh(db_comment)
    return db_comment


@router.delete("/{comment_id}")
def delete_comment(comment_id: int, db: Session = Depends(get_db)):
    """Delete comment"""
    db_comment = db.query(Comment).filter(Comment.id == comment_id).first()
    if not db_comment:
        raise HTTPException(status_code=404, detail="Comment not found")

    db.delete(db_comment)
    db.commit()
    return {"message": "Comment deleted"}
