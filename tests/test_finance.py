from unittest import TestCase
from unittest.mock import patch

from tickers import finance


class TestFinance(TestCase):
  @patch('yfinance.Ticker')
  def test_get_isin(self, mock_ticker):
    mock_ticker.return_value.info = {
      'longName': 'Horns & Hooves Co.',
      'symbol': 'HHVS',
      'exchange': 'NASDAQ',
    }
    security = finance.get_security_by_isin('US012345')
    self.assertEqual(security.full_name, 'Horns & Hooves Co.')
    self.assertEqual(security.symbol, 'HHVS')
    self.assertEqual(security.display_symbol, 'HHVS')
    self.assertEqual(security.namespace, 'NASDAQ')
    self.assertEqual(security.isin, 'US012345')
    self.assertEqual(security.fraction_reciprocal, 10000)

  @patch('yfinance.Ticker')
  def test_get_isin_missing_name(self, mock_ticker):
    mock_ticker.return_value.info = {
      'symbol': 'HHVS',
      'exchange': 'NASDAQ',
    }
    security = finance.get_security_by_isin('US012345')
    self.assertEqual(security.full_name, 'US012345')
    self.assertEqual(security.symbol, 'HHVS')
    self.assertEqual(security.display_symbol, 'HHVS')
    self.assertEqual(security.namespace, 'NASDAQ')
    self.assertEqual(security.isin, 'US012345')
    self.assertEqual(security.fraction_reciprocal, 10000)

  @patch('yfinance.Ticker')
  def test_get_isin_missing_symbol(self, mock_ticker):
    mock_ticker.return_value.info = {
      'longName': 'Horns & Hooves Co.',
      'exchange': 'NASDAQ',
    }
    security = finance.get_security_by_isin('US012345')
    self.assertEqual(security.full_name, 'Horns & Hooves Co.')
    self.assertEqual(security.symbol, 'US012345')
    self.assertEqual(security.display_symbol, 'US012345')
    self.assertEqual(security.namespace, 'NASDAQ')
    self.assertEqual(security.isin, 'US012345')
    self.assertEqual(security.fraction_reciprocal, 10000)

  @patch('yfinance.Ticker')
  def test_get_isin_missing_exchange(self, mock_ticker):
    mock_ticker.return_value.info = {
      'longName': 'Horns & Hooves Co.',
      'symbol': 'HHVS',
    }
    security = finance.get_security_by_isin('US012345')
    self.assertEqual(security.full_name, 'Horns & Hooves Co.')
    self.assertEqual(security.symbol, 'HHVS')
    self.assertEqual(security.display_symbol, 'HHVS')
    self.assertEqual(security.namespace, 'Unknown')
    self.assertEqual(security.isin, 'US012345')
    self.assertEqual(security.fraction_reciprocal, 10000)


# vim: ts=2:sw=2:et
