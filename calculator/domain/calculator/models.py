"""Calculator data models."""

import typing

import pydantic


class Operand(int):
    """Operand class to better represent negative integers."""

    def __str__(self):
        """Wrap negative numbers with parenthesis."""
        s = super().__str__()

        if self < 0:
            s = f"({s})"

        return s


class Operands(pydantic.BaseModel):
    """Operands data model."""

    left: Operand
    right: Operand


class Operation(pydantic.BaseModel):
    """Operation data model."""

    operands: Operands
    name: str
    symbol: str
    result: int
    expression: typing.Optional[str] = None

    @property
    def _expression(self) -> str:
        """Represent the operation as a mathematical expression.

        Example: "3 - (-2) = 5"

        Returns:
            str: mathematical expression form of the operation
        """
        return (
            f"{Operand(self.operands.left)}"
            f" {self.symbol}"
            f" {Operand(self.operands.right)}"
            f" ="
            f" {self.result}"
        )

    def __init__(self, *args, **kwargs):
        """Override pydantic.BaseModel constructor to include `expression`.

        Note that pydantic does not support computed properties yet (expected in v2).
        Here we are assigning `expression` attribute to `_expression` property
        so that it is included in the `dict` representation of the model.
        """
        super().__init__(*args, **kwargs)

        self.expression = self._expression
