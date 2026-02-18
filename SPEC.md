# Blog API

## Models
- Author: id, name, email, bio
- Post: id, title, content, author_id, status (draft/published),
  created_at, updated_at
- Comment: id, post_id, author_name, content, created_at

## Endpoints
- CRUD for Author, Post, Comment
- GET /posts — with pagination and filters
- GET /authors/{id}/posts — author's articles
- POST /posts/{id}/publish — publish a draft

## Requirements
- FastAPI + SQLite
- Tests (pytest)
- Docker
- README with examples