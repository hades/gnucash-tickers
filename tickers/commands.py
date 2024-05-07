from cleo.io import io as cleo_io
from cleo.ui import confirmation_question
from cleo.ui import table as cleo_table

from .data import Security
from .finance import get_security_by_isin
from .gnucash_wrapper import GnucashWrapper


def fsipdi(string: str):
  return "\u2068" + string + "\u2069"

def render_security_list(securities: list[Security], io: cleo_io.IO):
  table = cleo_table.Table(io)
  table.set_headers(["Namespace", "Name", "Symbol", "Display Symbol", "ISIN", "Fraction"])
  for security in securities:
    table.add_row([
      fsipdi(security.namespace),
      fsipdi(security.full_name),
      fsipdi(security.symbol),
      fsipdi(security.display_symbol),
      fsipdi(security.isin),
      f"1/{security.fraction_reciprocal}",
    ])
  table.render()

def add_cmd(wrapper: GnucashWrapper, book_filename: str, isin: str, confirm: bool, io: cleo_io.IO):
  security = get_security_by_isin(isin)
  if confirm:
    render_security_list([security], io)
    confirmation = confirmation_question.ConfirmationQuestion("Do you want to add this security?", False)
    if not confirmation.ask(io):
      return
  wrapper.add_securities(book_filename, [security])

def list_cmd_verbose(wrapper: GnucashWrapper, book_filename: str, io: cleo_io.IO):
  render_security_list(list(wrapper.iter_securities(book_filename)), io)

def list_cmd(wrapper: GnucashWrapper, book_filename: str, io: cleo_io.IO):
  if io.is_verbose():
    return list_cmd_verbose(wrapper, book_filename, io)
  for security in wrapper.iter_securities(book_filename):
    io.write_line(f"{security.namespace}/{security.full_name}")

# vim: ts=2:sw=2:et
