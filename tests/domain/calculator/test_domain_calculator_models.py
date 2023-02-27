import pydantic
import pytest

from calculator.domain.calculator.models import Operand
from calculator.domain.calculator.models import Operands
from calculator.domain.calculator.models import Operation


class TestOperand:
    @pytest.mark.parametrize(
        "value",
        [0, 1, 2, 3, 10, 100],
    )
    def test_nonnegative_integer(self, value):
        v = Operand(value)
        assert str(v) == str(value)

    @pytest.mark.parametrize(
        "value",
        [-1, -2, -3, -10, -100],
    )
    def test_negative_integer(self, value):
        v = Operand(value)
        assert str(v) == f"({value})"


class TestOperands:
    @pytest.mark.parametrize(
        "left,right",
        [
            (0, 0),
            (1, 1),
            ("2", "3"),
            ("-10", "-23"),
        ],
    )
    def test_valid_data(self, left, right):
        instance = Operands(left=left, right=right)

        assert instance.left == int(left)
        assert instance.right == int(right)

        d = instance.dict()

        assert len(d) == 2
        assert "left" in d
        assert "right" in d

    @pytest.mark.parametrize(
        "left,right",
        [
            ("a", 0),
            (0, "a"),
            ("5.3", "2.3"),
        ],
    )
    def test_invalid_data(self, left, right):
        with pytest.raises(pydantic.ValidationError):
            Operands(left=left, right=right)


class TestOperations:
    @pytest.mark.parametrize(
        "left,right,name,symbol,result,expression",
        [
            (0, 0, "addition", "+", 0, "0 + 0 = 0"),
            (3, 1, "subtraction", "-", 2, "3 - 1 = 2"),
        ],
    )
    def test_valid_data(self, left, right, name, symbol, result, expression):
        instance = Operation(
            operands=Operands(left=left, right=right),
            name=name,
            symbol=symbol,
            result=result,
        )

        assert instance.operands.left == left
        assert instance.operands.right == right
        assert instance.name == name
        assert instance.symbol == symbol
        assert instance.result == result
        assert instance.expression == expression

        d = instance.dict()

        assert len(d) == 5
        assert "operands" in d
        assert "name" in d
        assert "symbol" in d
        assert "result" in d
        assert "expression" in d

    @pytest.mark.parametrize(
        "left,right,name,symbol,result",
        [
            ("a", 0, "addition", "+", 0),
            (0, "a", "addition", "+", 0),
            (0, 0, "addition", "+", "a"),
        ],
    )
    def test_invalid_data(self, left, right, name, symbol, result):
        with pytest.raises(pydantic.ValidationError):
            Operation(
                operands=Operands(left=left, right=right),
                name=name,
                symbol=symbol,
                result=result,
            )
