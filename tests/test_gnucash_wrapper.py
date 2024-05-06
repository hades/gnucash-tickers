import contextlib
from unittest import TestCase
from unittest.mock import Mock

from tickers.gnucash_wrapper import GnucashWrapper


class MockSession:
  def __init__(self, book):
    self.book = book
    self.close = Mock()

def mock_book(commodity_table):
  book = Mock()
  table = Mock()
  book.get_table.return_value = table
  namespaces = []
  for namespace_name in commodity_table:
    namespace_obj = Mock()
    namespace_obj.get_gui_name.return_value = namespace_name
    commodities = []
    for commodity in commodity_table[namespace_name]:
      commodity_obj = Mock()
      commodity_obj.get_fullname.return_value = commodity[0]
      commodity_obj.get_user_symbol.return_value = commodity[1]
      commodity_obj.get_nice_symbol.return_value = commodity[2]
      commodity_obj.get_cusip.return_value = commodity[3]
      commodity_obj.get_fraction.return_value = commodity[4]
      commodities.append(commodity_obj)
    namespace_obj.get_commodity_list.return_value = commodities
    namespaces.append(namespace_obj)
  table.get_namespaces_list.return_value = namespaces
  return book

def mock_opener(book):
  return Mock(return_value=contextlib.closing(MockSession(book)))

class TestGnucashWrapper(TestCase):
  def test_iter_securities(self):
    wrapper = GnucashWrapper(mock_opener(mock_book({
        'NASDAQ': (
          ('Horns & Hooves Co.', 'HHVS', 'HORNS', 'US012345', 100),
          ('Very Good Construction Co.', 'VERY', 'VG', 'US000010', 1),
        ),
        'FRANKFURT': (
          ('Schweinewasser Import Export GmbH', 'SCHW', 'WASS', 'DE123456', 10000),
          ('Volkshochschulwagen', 'VHSW', 'WSHV', 'DE987361', 10),
          (None, None, None, None, None),
        ),
})))
    securities = list(wrapper.iter_securities("book.gnucash"))
    self.assertEqual(securities[0].full_name, 'Horns & Hooves Co.')
    self.assertEqual(securities[0].symbol, 'HHVS')
    self.assertEqual(securities[0].display_symbol, 'HORNS')
    self.assertEqual(securities[0].namespace, 'NASDAQ')
    self.assertEqual(securities[0].isin, 'US012345')
    self.assertEqual(securities[0].fraction_reciprocal, 100)
    self.assertEqual(securities[1].full_name, 'Very Good Construction Co.')
    self.assertEqual(securities[1].symbol, 'VERY')
    self.assertEqual(securities[1].display_symbol, 'VG')
    self.assertEqual(securities[1].namespace, 'NASDAQ')
    self.assertEqual(securities[1].isin, 'US000010')
    self.assertEqual(securities[1].fraction_reciprocal, 1)
    self.assertEqual(securities[2].full_name, 'Schweinewasser Import Export GmbH')
    self.assertEqual(securities[2].symbol, 'SCHW')
    self.assertEqual(securities[2].display_symbol, 'WASS')
    self.assertEqual(securities[2].namespace, 'FRANKFURT')
    self.assertEqual(securities[2].isin, 'DE123456')
    self.assertEqual(securities[2].fraction_reciprocal, 10000)
    self.assertEqual(securities[3].full_name, 'Volkshochschulwagen')
    self.assertEqual(securities[3].symbol, 'VHSW')
    self.assertEqual(securities[3].display_symbol, 'WSHV')
    self.assertEqual(securities[3].namespace, 'FRANKFURT')
    self.assertEqual(securities[3].isin, 'DE987361')
    self.assertEqual(securities[3].fraction_reciprocal, 10)
    self.assertEqual(securities[4].full_name, '')
    self.assertEqual(securities[4].symbol, '')
    self.assertEqual(securities[4].display_symbol, '')
    self.assertEqual(securities[4].namespace, 'FRANKFURT')
    self.assertEqual(securities[4].isin, '')
    self.assertEqual(securities[4].fraction_reciprocal, 1)
