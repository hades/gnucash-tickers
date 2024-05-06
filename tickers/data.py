from dataclasses import dataclass


@dataclass
class Security:
  full_name: str
  symbol: str
  display_symbol: str
  namespace: str
  isin: str
  fraction_reciprocal: int

# vim: ts=2:sw=2:et
