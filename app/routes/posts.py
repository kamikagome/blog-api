"""Post routes"""
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import Post, Author, PostStatus, Comment
from app.schemas import PostCreate, PostUpdate, Post as PostSchema, Comment as CommentSchema

router = APIRouter(prefix="/posts", tags=["posts"])


@router.post("", response_model=PostSchema)
def create_post(post: PostCreate, db: Session = Depends(get_db)):
    """Create a new post"""
    author = db.query(Author).filter(Author.id == post.author_id).first()
    if not author:
        raise HTTPException(status_code=404, detail="Author not found")

    db_post = Post(**post.model_dump())
    db.add(db_post)
    db.commit()
    db.refresh(db_post)
    return db_post


@router.get("", response_model=list[PostSchema])
def list_posts(
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
    status: str = Query(None),
    author_id: int = Query(None),
    db: Session = Depends(get_db)
):
    """List posts with pagination and filters"""
    query = db.query(Post)

    if status:
        if status not in [s.value for s in PostStatus]:
            raise HTTPException(status_code=400, detail="Invalid status")
        query = query.filter(Post.status == status)

    if author_id:
        query = query.filter(Post.author_id == author_id)

    return query.offset(skip).limit(limit).all()


@router.get("/{post_id}", response_model=PostSchema)
def get_post(post_id: int, db: Session = Depends(get_db)):
    """Get post by ID"""
    db_post = db.query(Post).filter(Post.id == post_id).first()
    if not db_post:
        raise HTTPException(status_code=404, detail="Post not found")
    return db_post


@router.put("/{post_id}", response_model=PostSchema)
def update_post(post_id: int, post: PostUpdate, db: Session = Depends(get_db)):
    """Update post"""
    db_post = db.query(Post).filter(Post.id == post_id).first()
    if not db_post:
        raise HTTPException(status_code=404, detail="Post not found")

    update_data = post.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_post, field, value)

    db.commit()
    db.refresh(db_post)
    return db_post


@router.delete("/{post_id}")
def delete_post(post_id: int, db: Session = Depends(get_db)):
    """Delete post"""
    db_post = db.query(Post).filter(Post.id == post_id).first()
    if not db_post:
        raise HTTPException(status_code=404, detail="Post not found")

    db.delete(db_post)
    db.commit()
    return {"message": "Post deleted"}


@router.post("/{post_id}/publish")
def publish_post(post_id: int, db: Session = Depends(get_db)):
    """Publish a draft post."""
    db_post = db.query(Post).filter(Post.id == post_id).first()
    if not db_post:
        raise HTTPException(status_code=404, detail="Post not found")

    if db_post.status == PostStatus.PUBLISHED:
        raise HTTPException(status_code=400, detail="Post is already published")

    db_post.status = PostStatus.PUBLISHED  # type: ignore
    db.commit()
    db.refresh(db_post)
    return db_post


@router.get("/{post_id}/comments", response_model=list[CommentSchema])
def get_post_comments(post_id: int, db: Session = Depends(get_db)):
    """Get all comments for a post"""
    post = db.query(Post).filter(Post.id == post_id).first()
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    return db.query(Comment).filter(Comment.post_id == post_id).all()


@router.post("/{post_id}/comments", response_model=CommentSchema)
def create_post_comment(post_id: int, comment: dict, db: Session = Depends(get_db)):
    """Create a comment on a post"""
    post = db.query(Post).filter(Post.id == post_id).first()
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")

    db_comment = Comment(
        post_id=post_id,
        author_name=comment.get("author_name"),
        content=comment.get("content")
    )
    db.add(db_comment)
    db.commit()
    db.refresh(db_comment)
    return db_comment
