from typing import Callable

from returns.io import IOResultE


def delete_user(remove: Callable[[str], IOResultE[None]], email: str) -> IOResultE[None]:
    return remove(email)
