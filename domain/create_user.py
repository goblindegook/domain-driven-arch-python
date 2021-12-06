from typing import Callable, List

from pydantic import EmailStr
from returns.io import IOResultE
from returns.pipeline import flow
from returns.curry import partial
from returns.pointfree import map_, bind_result, bind
from returns.result import safe, Failure, Success, ResultE

from domain.User import User


class DuplicateUserError(Exception):
    ...


def _duplicate_user_check(get_all: Callable[[], IOResultE[List[User]]], user: ResultE[User]) -> ResultE[User]:
    return flow(
        get_all(),
        map_(partial(map, lambda u: u.email)),
        bind(lambda emails: Failure(DuplicateUserError()) if user.email in emails else Success(user)),
    )


def create_user(
        get_all: Callable[[], IOResultE[List[User]]],
        put: Callable[[str, User], IOResultE[None]],
        email: EmailStr,
        name: str,
        password: str
) -> IOResultE[None]:
    return flow(
        safe(EmailStr.validate)(email),
        bind_result(lambda safe_email: safe(User)(email=safe_email, name=name, password=password)),
        bind_result(partial(_duplicate_user_check, get_all)),
        map_(lambda user: put(user.email, user))
    )
