"""Tests for all API endpoints"""
import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.database import get_db
from app.models import Base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Test database setup
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def override_get_db():
    """Override get_db for testing"""
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db


@pytest.fixture
def client():
    """Create test client and setup database"""
    Base.metadata.create_all(bind=engine)
    yield TestClient(app)
    Base.metadata.drop_all(bind=engine)


@pytest.fixture
def sample_author(client):
    """Create a sample author"""
    response = client.post(
        "/authors",
        json={
            "name": "John Doe",
            "email": "john@example.com",
            "bio": "A writer"
        }
    )
    return response.json()


@pytest.fixture
def sample_post(client, sample_author):
    """Create a sample post"""
    response = client.post(
        "/posts",
        json={
            "title": "Test Post",
            "content": "This is a test post",
            "author_id": sample_author["id"]
        }
    )
    return response.json()


class TestRoot:
    """Test root endpoints"""

    def test_root(self, client):
        """Test root endpoint"""
        response = client.get("/")
        assert response.status_code == 200
        assert "message" in response.json()
        assert "docs" in response.json()

    def test_health(self, client):
        """Test health check endpoint"""
        response = client.get("/health")
        assert response.status_code == 200
        assert response.json()["status"] == "healthy"


class TestAuthors:
    """Test author endpoints"""

    def test_create_author(self, client):
        """Test creating an author"""
        response = client.post(
            "/authors",
            json={
                "name": "Jane Smith",
                "email": "jane@example.com",
                "bio": "An author"
            }
        )
        assert response.status_code == 200
        data = response.json()
        assert data["name"] == "Jane Smith"
        assert data["email"] == "jane@example.com"
        assert data["bio"] == "An author"
        assert "id" in data

    def test_create_author_duplicate_email(self, client, sample_author):
        """Test creating an author with duplicate email"""
        response = client.post(
            "/authors",
            json={
                "name": "Another Name",
                "email": sample_author["email"],
                "bio": "Duplicate email"
            }
        )
        assert response.status_code == 400
        assert "Email already registered" in response.json()["detail"]

    def test_get_author(self, client, sample_author):
        """Test getting an author by ID"""
        response = client.get(f"/authors/{sample_author['id']}")
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == sample_author["id"]
        assert data["name"] == sample_author["name"]
        assert data["email"] == sample_author["email"]

    def test_get_nonexistent_author(self, client):
        """Test getting a nonexistent author"""
        response = client.get("/authors/9999")
        assert response.status_code == 404
        assert "Author not found" in response.json()["detail"]

    def test_update_author(self, client, sample_author):
        """Test updating an author"""
        response = client.put(
            f"/authors/{sample_author['id']}",
            json={"name": "Updated Name", "bio": "Updated bio"}
        )
        assert response.status_code == 200
        data = response.json()
        assert data["name"] == "Updated Name"
        assert data["bio"] == "Updated bio"

    def test_delete_author(self, client, sample_author):
        """Test deleting an author"""
        response = client.delete(f"/authors/{sample_author['id']}")
        assert response.status_code == 200
        assert "Author deleted" in response.json()["message"]

        # Verify author is deleted
        response = client.get(f"/authors/{sample_author['id']}")
        assert response.status_code == 404

    def test_get_author_posts(self, client, sample_author, sample_post):
        """Test getting author's posts"""
        response = client.get(f"/authors/{sample_author['id']}/posts")
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 1
        assert data[0]["title"] == sample_post["title"]


class TestPosts:
    """Test post endpoints"""

    def test_create_post(self, client, sample_author):
        """Test creating a post"""
        response = client.post(
            "/posts",
            json={
                "title": "New Post",
                "content": "New content",
                "author_id": sample_author["id"]
            }
        )
        assert response.status_code == 200
        data = response.json()
        assert data["title"] == "New Post"
        assert data["content"] == "New content"
        assert data["author_id"] == sample_author["id"]
        assert data["status"] == "draft"

    def test_create_post_nonexistent_author(self, client):
        """Test creating a post for a nonexistent author"""
        response = client.post(
            "/posts",
            json={
                "title": "Post",
                "content": "Content",
                "author_id": 9999
            }
        )
        assert response.status_code == 404
        assert "Author not found" in response.json()["detail"]

    def test_list_posts(self, client, sample_post):
        """Test listing posts"""
        response = client.get("/posts")
        assert response.status_code == 200
        data = response.json()
        assert len(data) > 0
        assert data[0]["title"] == sample_post["title"]

    def test_list_posts_pagination(self, client, sample_author):
        """Test posts pagination"""
        # Create multiple posts
        for i in range(5):
            client.post(
                "/posts",
                json={
                    "title": f"Post {i}",
                    "content": f"Content {i}",
                    "author_id": sample_author["id"]
                }
            )

        response = client.get("/posts?skip=0&limit=2")
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 2

        response = client.get("/posts?skip=2&limit=2")
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 2

    def test_list_posts_filter_by_status(self, client, sample_post):
        """Test filtering posts by status"""
        response = client.get("/posts?status=draft")
        assert response.status_code == 200
        data = response.json()
        assert len(data) > 0
        assert all(post["status"] == "draft" for post in data)

    def test_list_posts_filter_by_author(self, client, sample_post, sample_author):
        """Test filtering posts by author"""
        response = client.get(f"/posts?author_id={sample_author['id']}")
        assert response.status_code == 200
        data = response.json()
        assert len(data) > 0
        assert all(post["author_id"] == sample_author["id"] for post in data)

    def test_list_posts_invalid_status(self, client):
        """Test filtering with invalid status"""
        response = client.get("/posts?status=invalid")
        assert response.status_code == 400
        assert "Invalid status" in response.json()["detail"]

    def test_get_post(self, client, sample_post):
        """Test getting a post"""
        response = client.get(f"/posts/{sample_post['id']}")
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == sample_post["id"]
        assert data["title"] == sample_post["title"]

    def test_get_nonexistent_post(self, client):
        """Test getting a nonexistent post"""
        response = client.get("/posts/9999")
        assert response.status_code == 404
        assert "Post not found" in response.json()["detail"]

    def test_update_post(self, client, sample_post):
        """Test updating a post"""
        response = client.put(
            f"/posts/{sample_post['id']}",
            json={
                "title": "Updated Title",
                "content": "Updated content"
            }
        )
        assert response.status_code == 200
        data = response.json()
        assert data["title"] == "Updated Title"
        assert data["content"] == "Updated content"

    def test_delete_post(self, client, sample_post):
        """Test deleting a post"""
        response = client.delete(f"/posts/{sample_post['id']}")
        assert response.status_code == 200
        assert "Post deleted" in response.json()["message"]

        # Verify post is deleted
        response = client.get(f"/posts/{sample_post['id']}")
        assert response.status_code == 404

    def test_publish_post(self, client, sample_post):
        """Test publishing a post"""
        response = client.post(f"/posts/{sample_post['id']}/publish")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "published"

    def test_publish_already_published_post(self, client, sample_post):
        """Test publishing an already published post"""
        # First publish
        client.post(f"/posts/{sample_post['id']}/publish")

        # Try to publish again
        response = client.post(f"/posts/{sample_post['id']}/publish")
        assert response.status_code == 400
        assert "already published" in response.json()["detail"]

    def test_publish_nonexistent_post(self, client):
        """Test publishing a nonexistent post"""
        response = client.post("/posts/9999/publish")
        assert response.status_code == 404
        assert "Post not found" in response.json()["detail"]


class TestComments:
    """Test comment endpoints"""

    def test_create_comment(self, client, sample_post):
        """Test creating a comment"""
        response = client.post(
            "/comments",
            json={
                "post_id": sample_post["id"],
                "author_name": "Commenter",
                "content": "Great post!"
            }
        )
        assert response.status_code == 200
        data = response.json()
        assert data["author_name"] == "Commenter"
        assert data["content"] == "Great post!"
        assert data["post_id"] == sample_post["id"]

    def test_create_comment_nonexistent_post(self, client):
        """Test creating a comment on nonexistent post"""
        response = client.post(
            "/comments",
            json={
                "post_id": 9999,
                "author_name": "Commenter",
                "content": "Comment"
            }
        )
        assert response.status_code == 404
        assert "Post not found" in response.json()["detail"]

    def test_get_comment(self, client, sample_post):
        """Test getting a comment"""
        # Create a comment first
        create_response = client.post(
            "/comments",
            json={
                "post_id": sample_post["id"],
                "author_name": "Test User",
                "content": "Test comment"
            }
        )
        comment_id = create_response.json()["id"]

        response = client.get(f"/comments/{comment_id}")
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == comment_id
        assert data["author_name"] == "Test User"

    def test_get_nonexistent_comment(self, client):
        """Test getting a nonexistent comment"""
        response = client.get("/comments/9999")
        assert response.status_code == 404
        assert "Comment not found" in response.json()["detail"]

    def test_delete_comment(self, client, sample_post):
        """Test deleting a comment"""
        # Create a comment first
        create_response = client.post(
            "/comments",
            json={
                "post_id": sample_post["id"],
                "author_name": "Test User",
                "content": "Test comment"
            }
        )
        comment_id = create_response.json()["id"]

        response = client.delete(f"/comments/{comment_id}")
        assert response.status_code == 200
        assert "Comment deleted" in response.json()["message"]

        # Verify comment is deleted
        response = client.get(f"/comments/{comment_id}")
        assert response.status_code == 404
