def test_delete_a_user(web_client):
    client = web_client()
    client.create({"email": "jake.jackson@fbi.gov", "name": "Jake Jackson", "password": "password"})
    client.create({"email": "john.doe@gmail.com", "name": "John Doe", "password": "password"})

    response = client.remove("jake.jackson@fbi.gov")

    assert response.status_code == 204
    assert client.get_all().json() == [
        {"name": "John Doe", "email": "john.doe@gmail.com"}
    ]


