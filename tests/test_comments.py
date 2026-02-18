"""Tests for comment endpoints"""
import pytest


@pytest.fixture
def author_and_post(client):
    """Create a test author and post"""
    author_response = client.post(
        "/authors",
        json={
            "name": "John Doe",
            "email": "john@example.com",
            "bio": "A passionate writer"
        }
    )
    author = author_response.json()

    post_response = client.post(
        "/posts",
        json={
            "title": "My First Post",
            "content": "This is the content of my first post",
            "author_id": author["id"]
        }
    )
    post = post_response.json()

    return author, post


def test_create_comment(client, author_and_post):
    """Test creating a comment"""
    author, post = author_and_post

    response = client.post(
        "/comments",
        json={
            "post_id": post["id"],
            "author_name": "Jane Smith",
            "content": "Great post!"
        }
    )
    assert response.status_code == 200
    data = response.json()
    assert data["author_name"] == "Jane Smith"
    assert data["content"] == "Great post!"


def test_create_comment_on_nonexistent_post(client):
    """Test creating a comment on non-existent post"""
    response = client.post(
        "/comments",
        json={
            "post_id": 999,
            "author_name": "Jane Smith",
            "content": "Great post!"
        }
    )
    assert response.status_code == 404


def test_get_comment(client, author_and_post):
    """Test getting a comment"""
    author, post = author_and_post

    create_response = client.post(
        "/comments",
        json={
            "post_id": post["id"],
            "author_name": "Jane Smith",
            "content": "Great post!"
        }
    )
    comment_id = create_response.json()["id"]

    response = client.get(f"/comments/{comment_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == comment_id
    assert data["author_name"] == "Jane Smith"


def test_update_comment(client, author_and_post):
    """Test updating a comment"""
    author, post = author_and_post

    create_response = client.post(
        "/comments",
        json={
            "post_id": post["id"],
            "author_name": "Jane Smith",
            "content": "Great post!"
        }
    )
    comment_id = create_response.json()["id"]

    response = client.put(
        f"/comments/{comment_id}",
        json={
            "author_name": "Jane Smith Updated",
            "content": "Updated comment"
        }
    )
    assert response.status_code == 200
    data = response.json()
    assert data["author_name"] == "Jane Smith Updated"
    assert data["content"] == "Updated comment"


def test_delete_comment(client, author_and_post):
    """Test deleting a comment"""
    author, post = author_and_post

    create_response = client.post(
        "/comments",
        json={
            "post_id": post["id"],
            "author_name": "Jane Smith",
            "content": "Great post!"
        }
    )
    comment_id = create_response.json()["id"]

    response = client.delete(f"/comments/{comment_id}")
    assert response.status_code == 200

    get_response = client.get(f"/comments/{comment_id}")
    assert get_response.status_code == 404
