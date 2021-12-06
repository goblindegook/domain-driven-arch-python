def test_create_a_user(web_client):
    client = web_client()
    response = client.create({"email": "jake.jackson@fbi.gov", "name": "Jake Jackson", "password": "password"})

    assert response.status_code == 201
    assert client.get_all().json() == [
        {"name": "Jake Jackson", "email": "jake.jackson@fbi.gov"}
    ]


def test_cannot_create_repeated_user(web_client):
    client = web_client()
    client.create({"email": "jake.jackson@fbi.gov", "name": "Jake Jackson", "password": "password"})

    response = client.create({"email": "jake.jackson@fbi.gov", "name": "Jake Jackson", "password": "password"})

    assert response.status_code == 409
    assert client.get_all().json() == [
        {"name": "Jake Jackson", "email": "jake.jackson@fbi.gov"}
    ]


def test_cannot_create_user_with_invalid_email(web_client):
    client = web_client()

    response = client.create({"email": "invalid", "name": "Jake Jackson", "password": "password"})

    assert response.status_code == 422
