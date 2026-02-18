# Blog API

A FastAPI-based blog management system with SQLite database, comprehensive CRUD operations, and Docker support.

## Features

- **Author Management**: Create, read, update, and delete authors
- **Post Management**: Full CRUD operations with draft/published status
- **Comments**: Add and manage comments on posts
- **Pagination & Filtering**: List posts with pagination and filter by status/author
- **REST API**: Complete RESTful API with automatic OpenAPI/Swagger documentation

## Tech Stack

- **FastAPI** - Modern web framework
- **SQLAlchemy** - ORM for database operations
- **SQLite** - Lightweight database
- **Pydantic** - Data validation
- **Pytest** - Testing framework
- **Docker** - Containerization

## Installation

### Local Development

1. Clone the repository
2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Run the server:
```bash
uvicorn app.main:app --reload
```

The API will be available at `http://localhost:8000`

### Using Docker

```bash
docker-compose up --build
```

The API will be available at `http://localhost:8000`

## API Documentation

Interactive API documentation is available at:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## Health Check & Root Endpoints

### Health Check
```bash
curl http://localhost:8000/health
```

Response:
```json
{
  "status": "healthy"
}
```

### Root Endpoint
```bash
curl http://localhost:8000/
```

Response:
```json
{
  "message": "Welcome to Blog API",
  "docs": "/docs",
  "openapi": "/openapi.json"
}
```

---

## API Endpoints & Examples

### Authors

#### Create an Author
```bash
curl -X POST "http://localhost:8000/authors" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "John Doe",
    "email": "john@example.com",
    "bio": "A passionate writer"
  }'
```

Response:
```json
{
  "id": 1,
  "name": "John Doe",
  "email": "john@example.com",
  "bio": "A passionate writer"
}
```

#### List All Authors
```bash
curl "http://localhost:8000/authors"
```

Response:
```json
[
  {
    "id": 1,
    "name": "John Doe",
    "email": "john@example.com",
    "bio": "A passionate writer"
  },
  {
    "id": 2,
    "name": "Jane Smith",
    "email": "jane@example.com",
    "bio": "Tech enthusiast"
  }
]
```

#### Get a Specific Author
```bash
curl "http://localhost:8000/authors/1"
```

Response:
```json
{
  "id": 1,
  "name": "John Doe",
  "email": "john@example.com",
  "bio": "A passionate writer",
  "posts": [
    {
      "id": 1,
      "title": "My First Blog Post",
      "content": "This is the content of my first post.",
      "author_id": 1,
      "status": "published",
      "created_at": "2024-01-15T10:30:00",
      "updated_at": "2024-01-15T10:30:00"
    }
  ]
}
```

#### Update an Author
```bash
curl -X PUT "http://localhost:8000/authors/1" \
  -H "Content-Type: application/json" \
  -d '{
    "bio": "Updated bio - now an expert writer"
  }'
```

Response:
```json
{
  "id": 1,
  "name": "John Doe",
  "email": "john@example.com",
  "bio": "Updated bio - now an expert writer"
}
```

#### Delete an Author
```bash
curl -X DELETE "http://localhost:8000/authors/1"
```

Response:
```json
{
  "message": "Author deleted"
}
```

#### Get All Posts by an Author
```bash
curl "http://localhost:8000/authors/1/posts"
```

Response:
```json
[
  {
    "id": 1,
    "title": "My First Blog Post",
    "content": "This is the content of my first post.",
    "author_id": 1,
    "status": "published",
    "created_at": "2024-01-15T10:30:00",
    "updated_at": "2024-01-15T10:30:00",
    "comments": []
  },
  {
    "id": 2,
    "title": "Second Post",
    "content": "Content of second post.",
    "author_id": 1,
    "status": "draft",
    "created_at": "2024-01-16T14:20:00",
    "updated_at": "2024-01-16T14:20:00",
    "comments": []
  }
]
```

---

### Posts

#### Create a Post (Draft by Default)
```bash
curl -X POST "http://localhost:8000/posts" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "My First Blog Post",
    "content": "This is the content of my first post.",
    "author_id": 1
  }'
```

Response:
```json
{
  "id": 1,
  "title": "My First Blog Post",
  "content": "This is the content of my first post.",
  "author_id": 1,
  "status": "draft",
  "created_at": "2024-01-15T10:30:00",
  "updated_at": "2024-01-15T10:30:00",
  "comments": []
}
```

#### List All Posts (with Pagination)
```bash
curl "http://localhost:8000/posts?skip=0&limit=10"
```

Response:
```json
[
  {
    "id": 1,
    "title": "My First Blog Post",
    "content": "This is the content of my first post.",
    "author_id": 1,
    "status": "published",
    "created_at": "2024-01-15T10:30:00",
    "updated_at": "2024-01-15T10:30:00",
    "comments": []
  }
]
```

#### List Posts with Status Filter
```bash
curl "http://localhost:8000/posts?status=published"
```

Response:
```json
[
  {
    "id": 1,
    "title": "My First Blog Post",
    "content": "This is the content of my first post.",
    "author_id": 1,
    "status": "published",
    "created_at": "2024-01-15T10:30:00",
    "updated_at": "2024-01-15T10:30:00",
    "comments": []
  }
]
```

#### List Posts by Draft Status
```bash
curl "http://localhost:8000/posts?status=draft"
```

#### List Posts by Author ID
```bash
curl "http://localhost:8000/posts?author_id=1"
```

#### List Posts with Combined Filters
```bash
curl "http://localhost:8000/posts?author_id=1&status=published&skip=0&limit=5"
```

#### Get a Specific Post
```bash
curl "http://localhost:8000/posts/1"
```

Response:
```json
{
  "id": 1,
  "title": "My First Blog Post",
  "content": "This is the content of my first post.",
  "author_id": 1,
  "status": "published",
  "created_at": "2024-01-15T10:30:00",
  "updated_at": "2024-01-15T10:30:00",
  "comments": [
    {
      "id": 1,
      "post_id": 1,
      "author_name": "Jane Smith",
      "content": "Great post! Very informative.",
      "created_at": "2024-01-15T10:35:00"
    }
  ]
}
```

#### Update a Post
```bash
curl -X PUT "http://localhost:8000/posts/1" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Updated Title",
    "content": "Updated content for the post."
  }'
```

Response:
```json
{
  "id": 1,
  "title": "Updated Title",
  "content": "Updated content for the post.",
  "author_id": 1,
  "status": "draft",
  "created_at": "2024-01-15T10:30:00",
  "updated_at": "2024-01-15T11:00:00",
  "comments": []
}
```

#### Publish a Draft Post
```bash
curl -X POST "http://localhost:8000/posts/1/publish"
```

Response:
```json
{
  "id": 1,
  "title": "My First Blog Post",
  "content": "This is the content of my first post.",
  "author_id": 1,
  "status": "published",
  "created_at": "2024-01-15T10:30:00",
  "updated_at": "2024-01-15T10:35:00",
  "comments": []
}
```

#### Delete a Post
```bash
curl -X DELETE "http://localhost:8000/posts/1"
```

Response:
```json
{
  "message": "Post deleted"
}
```

---

### Comments

#### Create a Comment (via comments endpoint)
```bash
curl -X POST "http://localhost:8000/comments" \
  -H "Content-Type: application/json" \
  -d '{
    "post_id": 1,
    "author_name": "Jane Smith",
    "content": "Great post! Very informative."
  }'
```

Response:
```json
{
  "id": 1,
  "post_id": 1,
  "author_name": "Jane Smith",
  "content": "Great post! Very informative.",
  "created_at": "2024-01-15T10:35:00"
}
```

#### Create a Comment (via post endpoint)
```bash
curl -X POST "http://localhost:8000/posts/1/comments" \
  -H "Content-Type: application/json" \
  -d '{
    "author_name": "Jane Smith",
    "content": "Great post! Very informative."
  }'
```

Response:
```json
{
  "id": 1,
  "post_id": 1,
  "author_name": "Jane Smith",
  "content": "Great post! Very informative.",
  "created_at": "2024-01-15T10:35:00"
}
```

#### Get All Comments on a Post
```bash
curl "http://localhost:8000/posts/1/comments"
```

Response:
```json
[
  {
    "id": 1,
    "post_id": 1,
    "author_name": "Jane Smith",
    "content": "Great post! Very informative.",
    "created_at": "2024-01-15T10:35:00"
  },
  {
    "id": 2,
    "post_id": 1,
    "author_name": "Bob Johnson",
    "content": "Thanks for sharing!",
    "created_at": "2024-01-15T11:00:00"
  }
]
```

#### Get a Specific Comment
```bash
curl "http://localhost:8000/comments/1"
```

Response:
```json
{
  "id": 1,
  "post_id": 1,
  "author_name": "Jane Smith",
  "content": "Great post! Very informative.",
  "created_at": "2024-01-15T10:35:00"
}
```

#### Update a Comment
```bash
curl -X PUT "http://localhost:8000/comments/1" \
  -H "Content-Type: application/json" \
  -d '{
    "author_name": "Jane Smith",
    "content": "Updated comment - This is an excellent post!"
  }'
```

Response:
```json
{
  "id": 1,
  "post_id": 1,
  "author_name": "Jane Smith",
  "content": "Updated comment - This is an excellent post!",
  "created_at": "2024-01-15T10:35:00"
}
```

#### Delete a Comment
```bash
curl -X DELETE "http://localhost:8000/comments/1"
```

Response:
```json
{
  "message": "Comment deleted"
}
```

---

## Complete Workflow Example

Here's a complete example workflow demonstrating the API:

```bash
# 1. Create an author
AUTHOR=$(curl -s -X POST "http://localhost:8000/authors" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "John Doe",
    "email": "john@example.com",
    "bio": "A passionate writer"
  }')
echo $AUTHOR
AUTHOR_ID=$(echo $AUTHOR | grep -o '"id":[0-9]*' | head -1 | grep -o '[0-9]*')

# 2. Create a post (draft)
POST=$(curl -s -X POST "http://localhost:8000/posts" \
  -H "Content-Type: application/json" \
  -d "{
    \"title\": \"My First Post\",
    \"content\": \"This is my first blog post.\",
    \"author_id\": $AUTHOR_ID
  }")
echo $POST
POST_ID=$(echo $POST | grep -o '"id":[0-9]*' | head -1 | grep -o '[0-9]*')

# 3. Add a comment to the post
curl -s -X POST "http://localhost:8000/posts/$POST_ID/comments" \
  -H "Content-Type: application/json" \
  -d '{
    "author_name": "Reader",
    "content": "Great post!"
  }'

# 4. Publish the post
curl -s -X POST "http://localhost:8000/posts/$POST_ID/publish"

# 5. Retrieve the post with comments
curl -s "http://localhost:8000/posts/$POST_ID"

# 6. List all posts
curl -s "http://localhost:8000/posts"

# 7. Get author's posts
curl -s "http://localhost:8000/authors/$AUTHOR_ID/posts"
```

---

## Running Tests

```bash
pytest
```

For verbose output:
```bash
pytest -v
```

For coverage report:
```bash
pytest --cov=app
```

---

## API Endpoints Summary

### Authors
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/authors` | Create a new author |
| GET | `/authors` | List all authors |
| GET | `/authors/{id}` | Get an author by ID |
| PUT | `/authors/{id}` | Update an author |
| DELETE | `/authors/{id}` | Delete an author |
| GET | `/authors/{id}/posts` | Get all posts by an author |

### Posts
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/posts` | Create a new post (draft by default) |
| GET | `/posts` | List posts (with pagination and filters) |
| GET | `/posts/{id}` | Get a post by ID |
| PUT | `/posts/{id}` | Update a post |
| DELETE | `/posts/{id}` | Delete a post |
| POST | `/posts/{id}/publish` | Publish a draft post |
| GET | `/posts/{id}/comments` | Get all comments on a post |
| POST | `/posts/{id}/comments` | Create a comment on a post |

### Comments
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/comments` | Create a new comment |
| GET | `/comments/{id}` | Get a comment by ID |
| PUT | `/comments/{id}` | Update a comment |
| DELETE | `/comments/{id}` | Delete a comment |

---

## Query Parameters

### Posts Listing
- `skip` (int, default=0): Number of records to skip
- `limit` (int, default=10, max=100): Number of records to return
- `status` (string, optional): Filter by status ("draft" or "published")
- `author_id` (int, optional): Filter by author ID

**Example:**
```bash
curl "http://localhost:8000/posts?skip=0&limit=20&status=published&author_id=1"
```

---

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

---

## Project Structure

```
blog_api/
├── app/
│   ├── __init__.py
│   ├── main.py              # FastAPI application and main routes
│   ├── config.py            # Application configuration
│   ├── database.py          # Database setup and session management
│   ├── models.py            # SQLAlchemy database models
│   ├── schemas.py           # Pydantic validation schemas
│   └── routes/
│       ├── __init__.py
│       ├── authors.py       # Author endpoints
│       ├── posts.py         # Post endpoints
│       └── comments.py      # Comment endpoints
├── tests/
│   └── test_*.py            # Pytest test files
├── main.py                  # Entry point (imports from app.main)
├── Dockerfile               # Docker configuration
├── docker-compose.yml       # Docker Compose setup
├── requirements.txt         # Python dependencies
├── README.md                # This file
├── SPEC.md                  # API specification
└── blog.db                  # SQLite database (auto-created)
```

---

## Database

The application uses SQLite for persistent data storage. The database file (`blog.db`) is automatically created on first run.

### Database Relationships
- **Author** → **Posts**: One-to-many relationship
- **Post** → **Comments**: One-to-many relationship
- **Comment** references Post and Author indirectly

---

## Environment Variables

Configuration is managed through the `app/config.py` file. Key settings:
- `APP_NAME`: Application name (default: "Blog API")
- `DATABASE_URL`: Database connection string (default: "sqlite:///blog.db")

---

## Error Handling

The API returns standard HTTP status codes and error messages:

- **200 OK**: Successful GET request
- **201 Created**: Successful POST request
- **204 No Content**: Successful DELETE request
- **400 Bad Request**: Invalid input or business logic error
- **404 Not Found**: Resource not found
- **500 Internal Server Error**: Server error

Error response format:
```json
{
  "detail": "Error description"
}
```

---

## License

MIT License
# blog-api
