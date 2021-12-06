from functools import reduce
from typing import Dict

from fastapi import FastAPI

from domain.User import User
from web.list_users_handler import list_users_handler
from web.create_user_handler import create_user_handler
from web.delete_user_handler import delete_user_handler


def create_app(users: Dict[str, User]) -> FastAPI:
    return reduce(lambda _app, fn: fn(_app), [
        list_users_handler(users),
        create_user_handler(users),
        delete_user_handler(users),
    ], FastAPI())


app = create_app(users={})
