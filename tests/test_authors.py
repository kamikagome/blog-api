"""Tests for author endpoints"""


def test_create_author(client):
    """Test creating an author"""
    response = client.post(
        "/authors",
        json={
            "name": "John Doe",
            "email": "john@example.com",
            "bio": "A passionate writer"
        }
    )
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "John Doe"
    assert data["email"] == "john@example.com"
    assert data["bio"] == "A passionate writer"


def test_create_duplicate_email(client):
    """Test creating author with duplicate email"""
    client.post(
        "/authors",
        json={
            "name": "John Doe",
            "email": "john@example.com",
            "bio": "A passionate writer"
        }
    )
    response = client.post(
        "/authors",
        json={
            "name": "Jane Doe",
            "email": "john@example.com",
            "bio": "Another writer"
        }
    )
    assert response.status_code == 400


def test_get_author(client):
    """Test getting an author"""
    create_response = client.post(
        "/authors",
        json={
            "name": "John Doe",
            "email": "john@example.com",
            "bio": "A passionate writer"
        }
    )
    author_id = create_response.json()["id"]

    response = client.get(f"/authors/{author_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == author_id
    assert data["name"] == "John Doe"


def test_get_nonexistent_author(client):
    """Test getting a non-existent author"""
    response = client.get("/authors/999")
    assert response.status_code == 404


def test_update_author(client):
    """Test updating an author"""
    create_response = client.post(
        "/authors",
        json={
            "name": "John Doe",
            "email": "john@example.com",
            "bio": "A passionate writer"
        }
    )
    author_id = create_response.json()["id"]

    response = client.put(
        f"/authors/{author_id}",
        json={"name": "Jane Doe", "bio": "Updated bio"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Jane Doe"
    assert data["bio"] == "Updated bio"


def test_delete_author(client):
    """Test deleting an author"""
    create_response = client.post(
        "/authors",
        json={
            "name": "John Doe",
            "email": "john@example.com",
            "bio": "A passionate writer"
        }
    )
    author_id = create_response.json()["id"]

    response = client.delete(f"/authors/{author_id}")
    assert response.status_code == 200

    get_response = client.get(f"/authors/{author_id}")
    assert get_response.status_code == 404


def test_list_authors(client):
    """Test listing all authors"""
    client.post(
        "/authors",
        json={
            "name": "John Doe",
            "email": "john@example.com",
            "bio": "A passionate writer"
        }
    )
    client.post(
        "/authors",
        json={
            "name": "Jane Smith",
            "email": "jane@example.com",
            "bio": "Another writer"
        }
    )

    response = client.get("/authors")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2
    assert data[0]["name"] == "John Doe"
    assert data[1]["name"] == "Jane Smith"


def test_get_author_posts(client):
    """Test getting all posts by an author"""
    author_response = client.post(
        "/authors",
        json={
            "name": "John Doe",
            "email": "john@example.com",
            "bio": "A passionate writer"
        }
    )
    author_id = author_response.json()["id"]

    client.post(
        "/posts",
        json={
            "title": "Post 1",
            "content": "Content 1",
            "author_id": author_id
        }
    )
    client.post(
        "/posts",
        json={
            "title": "Post 2",
            "content": "Content 2",
            "author_id": author_id
        }
    )

    response = client.get(f"/authors/{author_id}/posts")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2
    assert data[0]["title"] == "Post 1"
    assert data[1]["title"] == "Post 2"
