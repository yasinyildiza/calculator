"""Multiplication operation."""

from calculator.domain.calculator.operator import Operator


class Multiplication(Operator):
    """Multiplication implementation."""

    name = "multiplication"
    symbol = "*"

    def compute(self) -> int:
        """Compute the result of multiplication operation.

        Returns:
            int: the result of the operation
        """
        return self.left * self.right
