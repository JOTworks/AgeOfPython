import sys

sys.path.append("./src")
sys.path.append("../src")
sys.path.append("./Tests/test_ai_files")
from main import main
import pytest

@pytest.mark.xfail(reason="Feature not implemented")
def test_replaced_JumpType():
    final_string = main([".\src\Main.py", "if_code.py", "-t"])
    assert "JumpType" not in final_string, "JumpType is not replaced"
