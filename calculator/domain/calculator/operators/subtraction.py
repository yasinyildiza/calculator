"""Substraction operation."""

from calculator.domain.calculator.operator import Operator


class Subtraction(Operator):
    """Substraction implementation."""

    name = "subtraction"
    symbol = "-"

    def compute(self) -> int:
        """Compute the result of substraction operation.

        Returns:
            int: the result of the operation
        """
        return self.left - self.right
