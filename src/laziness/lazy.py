import sys
from collections.abc import Callable, Mapping
from typing import Any

from _laziness import lazy_hook

__all__ = "lazify", "lazy"


def lazy(
    source: str,
    /,
    *,
    globals: dict[str, Any] | None = None,
    locals: Mapping[str, object] | None = None,
) -> Any:
    """
    Return an object that evaluates `source` upon access.
    """

    frame = sys._getframe(1)

    def _hook(*_: Any) -> Any:
        return eval(
            source, locals=locals or frame.f_locals, globals=globals or frame.f_globals
        )

    return lazy_hook(_hook, source)


def lazify[T](expression: Callable[[], T], /) -> T:
    """
    Return an object that evaluates `expression()` upon access.
    """

    def _hook(*_: Any) -> Any:
        return expression()

    name = getattr(expression, "__name__", "lazify")
    return lazy_hook(_hook, name)
