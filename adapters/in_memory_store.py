from typing import List, Dict, TypeVar

from returns.curry import curry
from returns.io import impure_safe

T = TypeVar("T")


@impure_safe
def get_all(store: Dict[str, T]) -> List[T]:
    return list(store.values())


@curry
@impure_safe
def put(store: Dict[str, T], key: str, value: T) -> None:
    store[key] = value


@curry
@impure_safe
def remove(store: Dict[str, T], key: str) -> None:
    store.pop(key)