"""Division operation."""

from calculator.domain.calculator.operator import Operator


class Division(Operator):
    """Division implementation."""

    name = "division"
    symbol = "//"

    def compute(self) -> int:
        """Compute the result of division operation.

        Returns:
            int: the result of the operation
        """
        return self.left // self.right
