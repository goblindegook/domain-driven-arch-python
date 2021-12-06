from typing import Dict

from fastapi import FastAPI
from returns.pipeline import flow
from returns.curry import curry, partial
from returns.unsafe import unsafe_perform_io
from starlette.status import HTTP_204_NO_CONTENT

from adapters.in_memory_store import remove
from domain.User import User
from domain.delete_user import delete_user


@curry
def delete_user_handler(users: Dict[str, User], app: FastAPI) -> FastAPI:
    _delete_user = partial(delete_user, remove(users))

    @app.delete("/users/{email}", status_code=HTTP_204_NO_CONTENT)
    async def handle(email: str):
        return flow(
            _delete_user(email),
            unsafe_perform_io,
            lambda r: r.value_or(None)
        )

    return app
