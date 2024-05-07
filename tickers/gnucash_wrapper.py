from collections.abc import Callable, Generator

import gnucash

from .data import Security


def none_to_empty_string(value):
  if isinstance(value, str):
    return value
  if value is None:
    return ""
  raise ValueError(f"Expected string or None, got {value!r}")

def int_or_default(value, default: int):
  if isinstance(value, int):
    return value
  if value is None:
    return default
  raise ValueError(f"Expected int or None, got {value!r}")

class GnucashWrapper:
  def __init__(self, session_opener: Callable[[str], gnucash.Session]):
    self.opener = session_opener

  @staticmethod
  def system():
    def opener(book_filename):
      return gnucash.Session(book_filename)
    return GnucashWrapper(opener)

  def add_securities(self, book_filename, securities: list[Security]):
    with self.opener(book_filename) as session:
      book = session.book
      table = book.get_table()
      for s in securities:
        table.insert(gnucash.GncCommodity(book, s.full_name, s.namespace,
                                          s.display_symbol, s.isin, s.fraction_reciprocal))

  def iter_securities(self, book_filename) -> Generator[Security, None, None]:
    with self.opener(book_filename) as session:
      book = session.book
      table = book.get_table()
      for ns in table.get_namespaces_list():
        for c in ns.get_commodity_list():
          yield Security(
              full_name=none_to_empty_string(c.get_fullname()),
              symbol=none_to_empty_string(c.get_user_symbol()),
              display_symbol=none_to_empty_string(c.get_nice_symbol()),
              namespace=none_to_empty_string(ns.get_gui_name()),
              isin=none_to_empty_string(c.get_cusip()),
              fraction_reciprocal=int_or_default(c.get_fraction(), 1))

# vim: ts=2:sw=2:et
