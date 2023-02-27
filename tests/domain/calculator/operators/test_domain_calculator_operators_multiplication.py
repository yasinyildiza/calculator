import pytest

from calculator.domain.calculator.models import Operation
from calculator.domain.calculator.operators.multiplication import Multiplication


class TestMultiplication:
    @pytest.mark.parametrize(
        "left,right,result,expression",
        [
            (3, 4, 12, "3 * 4 = 12"),
            (5, -8, -40, "5 * (-8) = -40"),
            (12, 4, 48, "12 * 4 = 48"),
        ],
    )
    def test(self, left, right, result, expression):
        operation: Operation = Multiplication(left=left, right=right).run()

        assert operation.operands.left == left
        assert operation.operands.right == right
        assert operation.name == "multiplication"
        assert operation.symbol == "*"
        assert operation.result == result
        assert operation.expression == expression
