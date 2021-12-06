from typing import Dict

from fastapi import FastAPI
from pydantic import BaseModel, EmailStr
from returns.curry import partial, curry
from returns.pipeline import flow
from returns.pointfree import alt
from starlette.responses import JSONResponse
from starlette.status import HTTP_201_CREATED, HTTP_409_CONFLICT, HTTP_500_INTERNAL_SERVER_ERROR

from adapters.in_memory_store import put, get_all
from domain.User import User
from domain.create_user import DuplicateUserError, create_user


@curry
def create_user_handler(users: Dict[str, User], app: FastAPI) -> FastAPI:
    _create_user = partial(create_user, partial(get_all, users), put(users))

    @app.post("/users")
    async def handle(user: _CreateUserBody):
        return flow(
            _create_user(user.email, user.name, user.password),
            alt(_error_to_status_code),
            lambda r: r.swap().value_or(JSONResponse(status_code=HTTP_201_CREATED)),
        )

    return app


class _CreateUserBody(BaseModel):
    email: EmailStr
    name: str
    password: str


def _error_to_status_code(err: Exception) -> JSONResponse:
    return {
        DuplicateUserError: JSONResponse(status_code=HTTP_409_CONFLICT),
        Exception: JSONResponse(status_code=HTTP_500_INTERNAL_SERVER_ERROR),
    }[type(err)]
