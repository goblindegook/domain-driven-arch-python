# Domain-driven Architecture in Python

## Why?

Check the [Kotlin version readme](https://github.com/lsoares/clean-architecture-sample).

## Commands

- Setup: get [Poetry](https://python-poetry.org) and `poetry install`
- Run app: `poetry run uvicorn web.main:app`
- Run tests: `poetry run pytest`
- Run tests in watch mode: `poetry run ptw`

## Challenge

1. The Grinch has secretly broken the code and the tests are not passing...
2. What are the uses cases, entities and ports? What are the primary adapters? And secondary?
3. Let's prevent repeated emails. Here's the test:
    ```python
    def test_cant_create_repeated_user():
        client = TestClient(WebApp(user_repository=UserRepositoryInMemory()))
        _create_user(client, "jake.jackson@fbi.gov", "Jake Jackson", "password")
    
        response = _create_user(client, "jake.jackson@fbi.gov", "Jake Jackson", "password")
    
        assert response.status_code == 409
        assert _list_users(client).json() == [
            {"name": "Jake Jackson", "email": "jake.jackson@fbi.gov"}
        ]
    ```
4. What does a port mean? What does it contain?
5. What's the advantage of the `UserRepository` port? What would you do to create and use an alternative
   to `UserRepositoryInMemory`?
6. Let's allow deleting a user. Here's the test:
    ```python
    def test_delete_a_user():
        client = TestClient(WebApp(user_repository=UserRepositoryInMemory()))
        _create_user(client, "jake.jackson@fbi.gov", "Jake Jackson", "password")
        _create_user(client, "john.doe@gmail.com", "John Doe", "password")
    
        response = _delete_user(client, "jake.jackson@fbi.gov")
        
        assert response.status_code == 204
        assert _list_users(client).json() == [
            {"name": "John Doe", "email": "john.doe@gmail.com"}
        ]
    
    def _delete_user(client, email: str):
        return client.delete(url=f"/users/{email}")
    ```
7. Why do we only test "as a user"? Don't we create domain tests? What's the trade-off?
8. Where would you put a CLI or a worker/job?
9. Why is `main.py` under `web`?
10. What are the upsides/downsides of having a use-case orientation? (separating use cases per file in the web and the
    domain)
11. Let's create a DSL for test usage
    (suggestion: create an `ApiClient` class and pass it the HTTP client)
