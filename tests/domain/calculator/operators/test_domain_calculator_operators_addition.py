import pytest

from calculator.domain.calculator.models import Operation
from calculator.domain.calculator.operators.addition import Addition


class TestAddition:
    @pytest.mark.parametrize(
        "left,right,result,expression",
        [
            (3, 4, 7, "3 + 4 = 7"),
            (5, -8, -3, "5 + (-8) = -3"),
            (12, 4, 16, "12 + 4 = 16"),
        ],
    )
    def test(self, left, right, result, expression):
        operation: Operation = Addition(left=left, right=right).run()

        assert operation.operands.left == left
        assert operation.operands.right == right
        assert operation.name == "addition"
        assert operation.symbol == "+"
        assert operation.result == result
        assert operation.expression == expression
