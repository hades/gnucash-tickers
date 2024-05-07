Gnucash Tickers
===============

This is a command-line tool to manipulate the Securities Database in Gnucash
books. Currently it supports listing securities, and adding a new security by
fetching its data by ISIN.

Prerequisites
-------------

To run this tool, you will need the following:

 * Python bindings for Gnucash,
 * Poetry.

Since Gnucash is not added explicitly as a dependency on this package, you will
have to enable system site packages access in Poetry:

```
$ poetry config virtualenvs.options.system-site-packages true
```

Distribution-Specific Instructions
----------------------------------

Feel free to add instructions for your operating system.

Ubuntu:

```sh
$ sudo apt-get install python3-gnucash python3-poetry gnucash
$ poetry config virtualenvs.options.system-site-packages true
$ poetry install --without=dev
```

Running
-------

Listing tickers in a book:

```sh
$ poetry run python -m tickers list book.gnucash -v
+--------------+-------------------------------------------+--------+----------------+--------------+-----------+
| Namespace    | Name                                      | Symbol | Display Symbol | ISIN         | Fraction  |
+--------------+-------------------------------------------+--------+----------------+--------------+-----------+
| template     | template                                  |        | template       | template     | 1/1       |
| Currencies   | Andorran Franc                            |        | ₣              | 950          | 1/100     |
...
```

Adding a ticker by its ISIN:

```sh
$ poetry run python -m tickers add test.gnucash US6903701018
+-----------+----------------+--------+----------------+----------------+----------+
| Namespace | Name           | Symbol | Display Symbol | ISIN           | Fraction |
+-----------+----------------+--------+----------------+----------------+----------+
| NYQ       | Beyond, Inc.   | BYON   | BYON           | US6903701018   | 1/10000  |
+-----------+----------------+--------+----------------+----------------+----------+
Do you want to add this security? (yes/no) [no] y
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
