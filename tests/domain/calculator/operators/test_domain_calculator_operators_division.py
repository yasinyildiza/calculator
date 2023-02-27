import pytest

from calculator.domain.calculator.models import Operation
from calculator.domain.calculator.operators.division import Division


class TestDivision:
    @pytest.mark.parametrize(
        "left,right,result,expression",
        [
            (3, 4, 0, "3 // 4 = 0"),
            (5, -8, -1, "5 // (-8) = -1"),
            (12, 4, 3, "12 // 4 = 3"),
        ],
    )
    def test(self, left, right, result, expression):
        operation: Operation = Division(left=left, right=right).run()

        assert operation.operands.left == left
        assert operation.operands.right == right
        assert operation.name == "division"
        assert operation.symbol == "//"
        assert operation.result == result
        assert operation.expression == expression
