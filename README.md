Gnucash Tickers
===============

TODO

Running
-------

```sh
$ poetry install --without=dev
$ poetry run python -m tickers list book.gnucash
```

Developing
----------

Please install the pre-commit hooks to make sure your code passes my very high
quality standards. /s

```sh
$ poetry install --with=dev
$ poetry run pre-commit install
```

Add unit tests for all new code.
