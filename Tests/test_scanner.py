from logging.config import IDENTIFIER
from Parser import Parcer
from Scanner import Scanner
from data import *


@pytest.mark.paramertrize("test_input,expected",[
('variableName', TokenType.IDENTIFIER)
])

def test_scanner(test_input, expected):
  myScanner = Scanner(None, None)
  myScanner.scanLine(test_input)
  assert len(myScanner.tokens) == 1
  assert myScanner.tokens[0].TokenType == expected
