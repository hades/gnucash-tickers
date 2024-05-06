import logging

from cleo.application import Application
from cleo.commands.command import Command
from cleo.io.inputs.argument import Argument
from cleo.io.inputs.option import Option

from .commands import list_cmd
from .gnucash_wrapper import GnucashWrapper


class CleoHandler(logging.Handler):
  def __init__(self, io):
    super().__init__()
    self.io = io
    self.setFormatter(logging.Formatter("<info>%(funcName)s:%(lineno)s: %(message)s"))

  def emit(self, record):
    self.io.write_line(self.format(record))

class ListCommand(Command):
  name = "list"
  arguments = [
    Argument("book_file", description="Path to the Gnucash book", required=True),
  ]
  options = [
    Option("debug", description="Enables debug output", flag=True),
  ]

  def _setup_debug_logging(self):
    handler = CleoHandler(self.io)
    handler.setLevel(logging.DEBUG)
    logging.getLogger().addHandler(handler)
    logging.getLogger().setLevel(logging.DEBUG)
    logging.debug("debug logging enabled")

  def handle(self):
    if self.option('debug'):
      self._setup_debug_logging()
    return list_cmd(GnucashWrapper.system(), self.argument('book_file'), self.io)


app = Application()
app.add(ListCommand())

app.run()

# vim: ts=2:sw=2:et
