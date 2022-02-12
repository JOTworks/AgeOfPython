from logging.config import IDENTIFIER
from AOEparser import Parcer
from AOEscanner import Scanner
from data import *
import pytest


@pytest.mark.paramertrize("test_input,expected",[
('variableName', TokenType.IDENTIFIER)
])

def test_scanner(test_input, expected):
  myScanner = Scanner(None, None)
  myScanner.scanLine(test_input)
  assert len(myScanner.tokens) == 1
  assert myScanner.tokens[0].TokenType == expected
