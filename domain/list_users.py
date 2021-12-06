from typing import Callable, List

from domain.User import User


def list_users(get_all: Callable[[], List[User]]) -> List[User]:
    return get_all()
