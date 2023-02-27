import pytest

from calculator.domain.calculator.models import Operation
from calculator.domain.calculator.operators.subtraction import Subtraction


class TestSubtraction:
    @pytest.mark.parametrize(
        "left,right,result,expression",
        [
            (3, 4, -1, "3 - 4 = -1"),
            (5, -8, 13, "5 - (-8) = 13"),
            (12, 4, 8, "12 - 4 = 8"),
        ],
    )
    def test(self, left, right, result, expression):
        operation: Operation = Subtraction(left=left, right=right).run()

        assert operation.operands.left == left
        assert operation.operands.right == right
        assert operation.name == "subtraction"
        assert operation.symbol == "-"
        assert operation.result == result
        assert operation.expression == expression
