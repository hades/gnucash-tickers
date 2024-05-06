from cleo.io import io as cleo_io
from cleo.ui import table as cleo_table

from .gnucash_wrapper import GnucashWrapper


def fsipdi(string: str):
  return "\u2068" + string + "\u2069"

def list_cmd_verbose(wrapper: GnucashWrapper, book_filename: str, io: cleo_io.IO):
  table = cleo_table.Table(io)
  table.set_headers(["Namespace", "Name", "Symbol", "Display Symbol", "ISIN", "Fraction"])
  for security in wrapper.iter_securities(book_filename):
    table.add_row([
      fsipdi(security.namespace),
      fsipdi(security.full_name),
      fsipdi(security.symbol),
      fsipdi(security.display_symbol),
      fsipdi(security.isin),
      f"1/{security.fraction_reciprocal}",
    ])
  table.render()

def list_cmd(wrapper: GnucashWrapper, book_filename: str, io: cleo_io.IO):
  if io.is_verbose():
    return list_cmd_verbose(wrapper, book_filename, io)
  for security in wrapper.iter_securities(book_filename):
    io.write_line(f"{security.namespace}/{security.full_name}")

# vim: ts=2:sw=2:et
