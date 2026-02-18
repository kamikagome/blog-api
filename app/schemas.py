"""Pydantic schemas for request/response validation"""
from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, EmailStr


class AuthorBase(BaseModel):
    """Base author schema"""
    name: str
    email: EmailStr
    bio: Optional[str] = None


class AuthorCreate(AuthorBase):
    """Schema for creating an author"""
    pass


class AuthorUpdate(BaseModel):
    """Schema for updating an author"""
    name: Optional[str] = None
    bio: Optional[str] = None


class Author(AuthorBase):
    """Author response schema"""
    id: int

    class Config:
        from_attributes = True


class PostBase(BaseModel):
    """Base post schema"""
    title: str
    content: str
    author_id: int


class PostCreate(PostBase):
    """Schema for creating a post"""
    pass


class PostUpdate(BaseModel):
    """Schema for updating a post"""
    title: Optional[str] = None
    content: Optional[str] = None
    status: Optional[str] = None


class CommentBase(BaseModel):
    """Base comment schema"""
    author_name: str
    content: str


class CommentCreate(CommentBase):
    """Schema for creating a comment"""
    post_id: int


class Comment(CommentBase):
    """Comment response schema"""
    id: int
    post_id: int
    created_at: datetime

    class Config:
        from_attributes = True


class Post(PostBase):
    """Post response schema"""
    id: int
    status: str
    created_at: datetime
    updated_at: datetime
    comments: List[Comment] = []

    class Config:
        from_attributes = True


class AuthorDetail(Author):
    """Author with posts"""
    posts: List[Post] = []

    class Config:
        from_attributes = True
