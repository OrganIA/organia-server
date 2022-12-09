def test_get_users(client):
    response = client.get('/api/users/')
    assert response.status_code == 200


def test_get_me(client):
    response = client.get('/api/users/me')
    assert response.status_code == 200


def test_get_user(client):
    response = client.get('/api/users/1')
    assert response.status_code == 200


data = {
    "firstname": "user",
    "lastname": "test",
    "email": "user@test.fr",
    "password": "test",
    "phone_number": "0660203526",
}

data_login = {"email": "user@test.fr", "password": "test"}


def test_register(client):
    response = client.post('/api/auth/register', json=data)
    assert response.status_code == 201


def test_login(client):
    response = client.post('/api/auth/login', json=data_login)
    assert response.status_code == 200


def test_delete_user(client):
    response = client.delete('/api/users/2')
    assert response.status_code == 204
