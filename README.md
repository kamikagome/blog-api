# Blog API

A FastAPI-based blog management system with SQLite database, comprehensive CRUD operations, and Docker support.

## Features

- **Author Management**: Create, read, update, and delete authors
- **Post Management**: Full CRUD with draft/published status
- **Comments**: Add and manage comments on posts
- **Pagination & Filtering**: List posts with pagination and filter by status/author
- **REST API**: Complete RESTful API with automatic Swagger documentation

## Tech Stack

- **FastAPI** - Web framework
- **SQLAlchemy** - ORM
- **SQLite** - Database
- **Pydantic** - Data validation
- **Pytest** - Testing
- **Docker** - Containerization

## Quick Start

### Local Development

```bash
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

API available at `http://localhost:8000`

### Docker

```bash
docker-compose up --build
```

## API Documentation

Interactive documentation available at:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## API Endpoints

### Authors
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/authors` | Create author |
| GET | `/authors` | List all authors |
| GET | `/authors/{id}` | Get author by ID |
| PUT | `/authors/{id}` | Update author |
| DELETE | `/authors/{id}` | Delete author |
| GET | `/authors/{id}/posts` | Get author's posts |

### Posts
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/posts` | Create post (draft by default) |
| GET | `/posts` | List posts with pagination/filters |
| GET | `/posts/{id}` | Get post by ID |
| PUT | `/posts/{id}` | Update post |
| DELETE | `/posts/{id}` | Delete post |
| POST | `/posts/{id}/publish` | Publish draft post |
| GET | `/posts/{id}/comments` | Get post comments |
| POST | `/posts/{id}/comments` | Add comment to post |

### Comments
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/comments` | Create comment |
| GET | `/comments/{id}` | Get comment by ID |
| PUT | `/comments/{id}` | Update comment |
| DELETE | `/comments/{id}` | Delete comment |

## Query Parameters

**Posts Listing:**
- `skip` (int, default=0): Records to skip
- `limit` (int, default=10, max=100): Records to return
- `status` (string): Filter by "draft" or "published"
- `author_id` (int): Filter by author ID

Example: `GET /posts?skip=0&limit=20&status=published&author_id=1`

## Data Models

### Author
```json
{
  "id": 1,
  "name": "string",
  "email": "string",
  "bio": "string"
}
```

### Post
```json
{
  "id": 1,
  "title": "string",
  "content": "string",
  "author_id": 1,
  "status": "draft or published",
  "created_at": "2024-01-15T10:30:00",
  "updated_at": "2024-01-15T10:30:00",
  "comments": []
}
```

### Comment
```json
{
  "id": 1,
  "post_id": 1,
  "author_name": "string",
  "content": "string",
  "created_at": "2024-01-15T10:35:00"
}
```

## Project Structure

```
blog_api/
├── app/
│   ├── main.py              # FastAPI app and routes
│   ├── config.py            # Configuration
│   ├── database.py          # Database setup
│   ├── models.py            # SQLAlchemy models
│   ├── schemas.py           # Pydantic schemas
│   └── routes/              # API endpoints
│       ├── authors.py
│       ├── posts.py
│       └── comments.py
├── tests/                   # Test files
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
└── blog.db                  # SQLite database (auto-created)
```

## Database

Uses SQLite with the following relationships:
- **Author** → **Posts**: One-to-many
- **Post** → **Comments**: One-to-many

Database file (`blog.db`) is auto-created on first run.

## Testing

```bash
pytest              # Run tests
pytest -v           # Verbose output
pytest --cov=app    # Coverage report
```

## License

MIT
