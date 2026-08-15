# laziness

Arbitrary lazy objects for Python 3.15 and above.

## Installation

```console
pip install laziness
```

## Usage

### `lazy`

`lazy` takes a positional string argument. It returns a special object that
will evaluate the string as a Python expression when accessed. For example:

```pycon
>>> from laziness import lazy
>>> foo = lazy("print(42) or 24")
>>> # foo has not been evaluated yet...
>>> foo
42
24
>>> # Evaluation only happens once
>>> foo
24
```

### `lazify`

`lazify` is similar to `lazy`, but instead of taking a string for the source,
it takes a callable. This callable is then invoked when the lazy object is accessed.
For example:

```pycon
>>> from laziness import lazify
>>> foo = lazify(lambda: print(42) or 24)
>>> foo
42
24
>>> foo
24
```

## Example

```pycon
from laziness import lazy, lazify

def expensive_work():
    import time
    time.sleep(1)
    return 42

EXPENSIVE_CONSTANT = lazy("expensive_work()")
EXPENSIVE_CONSTANT_ALT = lazify(lambda: expensive_work())

def public_function():
    # EXPENSIVE_CONSTANT is not evaluated until this function is called
    print(EXPENSIVE_CONSTANT)
```

## How it works

Python 3.15 introduces [lazy imports](https://docs.python.org/3.15/reference/simple_stmts.html#lazy-imports).
In CPython, this is implemented through a custom type that calls `__import__`
upon global lookup. This library builds on that functionality and takes it a
step further; instead of just calling `__import__`, you can call anything!

## License

`laziness` is distributed under the terms of the [MIT](https://spdx.org/licenses/MIT.html) license.
