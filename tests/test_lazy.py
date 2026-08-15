from typing import Any

from pytest import raises

from laziness import lazify, lazy


def _ignore(value: Any) -> None:
    """
    Resolve a lazy value through a namespace lookup and discard the result.
    """
    eval("value")


def test_lazy_evaluation():
    value = 0

    def evaluate():
        nonlocal value
        value += 1

    special = lazy("evaluate()")
    assert value == 0
    _ignore(special)
    assert value == 1

    special = lazify(evaluate)
    assert value == 1
    _ignore(special)


def test_lazy_exceptions():
    def kaboom():
        raise ZeroDivisionError

    special = lazy("kaboom()")

    with raises(ZeroDivisionError):
        _ignore(special)

    special = lazify(kaboom)
    with raises(ZeroDivisionError):
        _ignore(special)
