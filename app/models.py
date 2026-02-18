"""SQLAlchemy database models."""
from datetime import datetime
from typing import TYPE_CHECKING
import enum

from sqlalchemy import Column, DateTime, Enum, ForeignKey, Integer, String, Text
from sqlalchemy.orm import declarative_base, relationship

if TYPE_CHECKING:
    from sqlalchemy.orm import DeclarativeBase
else:

    class DeclarativeBase:
        """Placeholder for type checking."""

        pass


Base = declarative_base()  # type: ignore


class PostStatus(str, enum.Enum):
    """Post publication status."""

    DRAFT = "draft"
    PUBLISHED = "published"


class Author(Base):  # type: ignore
    """Author model."""

    __tablename__ = "authors"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False, index=True)
    email = Column(String(255), unique=True, nullable=False, index=True)
    bio = Column(Text, nullable=True)

    posts = relationship("Post", back_populates="author")


class Post(Base):  # type: ignore
    """Post model."""

    __tablename__ = "posts"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False, index=True)
    content = Column(Text, nullable=False)
    author_id = Column(Integer, ForeignKey("authors.id"), nullable=False, index=True)
    status: Column[Enum] = Column(
        Enum(PostStatus), default=PostStatus.DRAFT, nullable=False, index=True
    )
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    author = relationship("Author", back_populates="posts")
    comments = relationship("Comment", back_populates="post", cascade="all, delete-orphan")


class Comment(Base):  # type: ignore
    """Comment model."""

    __tablename__ = "comments"

    id = Column(Integer, primary_key=True, index=True)
    post_id = Column(Integer, ForeignKey("posts.id"), nullable=False, index=True)
    author_name = Column(String(255), nullable=False)
    content = Column(Text, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    post = relationship("Post", back_populates="comments")
