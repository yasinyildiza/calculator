"""Base Operator class."""

import abc

from calculator.domain.calculator.models import Operands
from calculator.domain.calculator.models import Operation


class Operator(abc.ABC):
    """Base Operator class.

    Attributes:
        name: unique name of the operation.
        symbol: mathematical symbol of the operation.
        left: left operand of the operation.
        right:right operand of the operation.
    """

    def __init__(self, left: int, right: int):
        """Initialize Operator with left and right operands."""
        self.left: int = left
        self.right: int = right

    @property
    @abc.abstractmethod
    def name(self) -> str:
        """Return the unique name of mathematical the operation."""

    @property
    @abc.abstractmethod
    def symbol(self) -> str:
        """Mathematical symbol of the operation, typically a single character."""

    @abc.abstractmethod
    def compute(self) -> int:
        """Compute the mathematical operation between operands and return the result.

        Returns:
            int: result of the mathematical operation.
        """

    def run(self) -> Operation:
        """Wrap the computation result along with operands and return Operation.

        Returns:
            Operation: the resultant operation object with all elements
        """
        return Operation(
            operands=Operands(left=self.left, right=self.right),
            name=self.name,
            symbol=self.symbol,
            result=self.compute(),
        )
