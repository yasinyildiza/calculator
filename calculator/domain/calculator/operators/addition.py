"""Addition operation."""

from calculator.domain.calculator.operator import Operator


class Addition(Operator):
    """Addition implementation."""

    name = "addition"
    symbol = "+"

    def compute(self) -> int:
        """Compute the result of addition operation.

        Returns:
            int: the result of the operation
        """
        return self.left + self.right
