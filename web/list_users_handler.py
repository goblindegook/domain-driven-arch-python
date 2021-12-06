from typing import Dict

from fastapi import FastAPI
from returns.pipeline import flow
from returns.curry import partial, curry
from returns.pointfree import map_
from returns.unsafe import unsafe_perform_io
from starlette.responses import JSONResponse

from adapters.in_memory_store import get_all
from domain.User import User
from domain.list_users import list_users


@curry
def list_users_handler(users: Dict[str, User], app: FastAPI) -> FastAPI:
    _list_users = partial(list_users, partial(get_all, users))

    @app.get("/users")
    async def handle():
        return flow(
            _list_users(),
            map_(partial(map, lambda u: {"name": u.name, "email": u.email})),
            map_(list),
            unsafe_perform_io,
            lambda r: r.value_or([]),
            JSONResponse,
        )

    return app