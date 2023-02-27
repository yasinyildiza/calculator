"""Operator registry."""

from calculator.core.registry import Registry
from calculator.domain.calculator import operators
from calculator.domain.calculator.operator import Operator


class OperatorRegistry(Registry):
    """Operator registry class to register operators by their name."""

    element_cls = Operator
    package = operators
    auto_collect = True
