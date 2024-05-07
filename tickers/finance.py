import yfinance

from .data import Security


def get_security_by_isin(isin: str):
  yf_ticker = yfinance.Ticker(isin)
  return Security(
    full_name=yf_ticker.info.get("longName") or isin,
    symbol=yf_ticker.info.get("symbol") or isin,
    display_symbol=yf_ticker.info.get("symbol") or isin,
    namespace=yf_ticker.info.get("exchange") or "Unknown",
    isin=isin,
    fraction_reciprocal=10000)
