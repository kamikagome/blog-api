"""Tests for post endpoints"""
import pytest


@pytest.fixture
def author(client):
    """Create a test author"""
    response = client.post(
        "/authors",
        json={
            "name": "John Doe",
            "email": "john@example.com",
            "bio": "A passionate writer"
        }
    )
    return response.json()


def test_create_post(client, author):
    """Test creating a post"""
    response = client.post(
        "/posts",
        json={
            "title": "My First Post",
            "content": "This is the content of my first post",
            "author_id": author["id"]
        }
    )
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "My First Post"
    assert data["status"] == "draft"


def test_create_post_with_nonexistent_author(client):
    """Test creating a post with non-existent author"""
    response = client.post(
        "/posts",
        json={
            "title": "My First Post",
            "content": "This is the content of my first post",
            "author_id": 999
        }
    )
    assert response.status_code == 404


def test_list_posts(client, author):
    """Test listing posts"""
    client.post(
        "/posts",
        json={
            "title": "Post 1",
            "content": "Content 1",
            "author_id": author["id"]
        }
    )
    client.post(
        "/posts",
        json={
            "title": "Post 2",
            "content": "Content 2",
            "author_id": author["id"]
        }
    )

    response = client.get("/posts")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2


def test_list_posts_with_pagination(client, author):
    """Test listing posts with pagination"""
    for i in range(15):
        client.post(
            "/posts",
            json={
                "title": f"Post {i+1}",
                "content": f"Content {i+1}",
                "author_id": author["id"]
            }
        )

    response = client.get("/posts?skip=0&limit=5")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 5


def test_list_posts_by_status(client, author):
    """Test listing posts filtered by status"""
    post_response = client.post(
        "/posts",
        json={
            "title": "My Draft",
            "content": "Draft content",
            "author_id": author["id"]
        }
    )
    post_id = post_response.json()["id"]

    client.post(f"/posts/{post_id}/publish")

    response = client.get("/posts?status=published")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["status"] == "published"


def test_get_post(client, author):
    """Test getting a post"""
    create_response = client.post(
        "/posts",
        json={
            "title": "My First Post",
            "content": "This is the content of my first post",
            "author_id": author["id"]
        }
    )
    post_id = create_response.json()["id"]

    response = client.get(f"/posts/{post_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == post_id
    assert data["title"] == "My First Post"


def test_update_post(client, author):
    """Test updating a post"""
    create_response = client.post(
        "/posts",
        json={
            "title": "My First Post",
            "content": "This is the content of my first post",
            "author_id": author["id"]
        }
    )
    post_id = create_response.json()["id"]

    response = client.put(
        f"/posts/{post_id}",
        json={"title": "Updated Title", "content": "Updated content"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Updated Title"


def test_publish_post(client, author):
    """Test publishing a post"""
    create_response = client.post(
        "/posts",
        json={
            "title": "My First Post",
            "content": "This is the content of my first post",
            "author_id": author["id"]
        }
    )
    post_id = create_response.json()["id"]

    response = client.post(f"/posts/{post_id}/publish")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "published"


def test_publish_already_published_post(client, author):
    """Test publishing an already published post"""
    create_response = client.post(
        "/posts",
        json={
            "title": "My First Post",
            "content": "This is the content of my first post",
            "author_id": author["id"]
        }
    )
    post_id = create_response.json()["id"]

    client.post(f"/posts/{post_id}/publish")
    response = client.post(f"/posts/{post_id}/publish")
    assert response.status_code == 400


def test_delete_post(client, author):
    """Test deleting a post"""
    create_response = client.post(
        "/posts",
        json={
            "title": "My First Post",
            "content": "This is the content of my first post",
            "author_id": author["id"]
        }
    )
    post_id = create_response.json()["id"]

    response = client.delete(f"/posts/{post_id}")
    assert response.status_code == 200

    get_response = client.get(f"/posts/{post_id}")
    assert get_response.status_code == 404


def test_create_comment_on_post(client, author):
    """Test creating a comment on a post"""
    create_post_response = client.post(
        "/posts",
        json={
            "title": "My First Post",
            "content": "This is the content of my first post",
            "author_id": author["id"]
        }
    )
    post_id = create_post_response.json()["id"]

    response = client.post(
        f"/posts/{post_id}/comments",
        json={
            "author_name": "Jane Smith",
            "content": "Great post!"
        }
    )
    assert response.status_code == 200
    data = response.json()
    assert data["author_name"] == "Jane Smith"
    assert data["content"] == "Great post!"
    assert data["post_id"] == post_id


def test_get_post_comments(client, author):
    """Test getting comments for a post"""
    create_post_response = client.post(
        "/posts",
        json={
            "title": "My First Post",
            "content": "This is the content of my first post",
            "author_id": author["id"]
        }
    )
    post_id = create_post_response.json()["id"]

    client.post(
        f"/posts/{post_id}/comments",
        json={
            "author_name": "Jane Smith",
            "content": "Great post!"
        }
    )
    client.post(
        f"/posts/{post_id}/comments",
        json={
            "author_name": "Bob Johnson",
            "content": "I agree!"
        }
    )

    response = client.get(f"/posts/{post_id}/comments")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2
    assert data[0]["author_name"] == "Jane Smith"
    assert data[1]["author_name"] == "Bob Johnson"
