from tests.api.v1.test_api_v1_calculator import TestAdd
from tests.api.v1.test_api_v1_calculator import TestDivide
from tests.api.v1.test_api_v1_calculator import TestMultiply
from tests.api.v1.test_api_v1_calculator import TestSubtract


class TestAddV2(TestAdd):
    endpoint = "/api/v2/calculator/addition"


class TestSubtractV2(TestSubtract):
    endpoint = "/api/v2/calculator/subtraction"


class TestMultiplyV2(TestMultiply):
    endpoint = "/api/v2/calculator/multiplication"


class TestDivideV2(TestDivide):
    endpoint = "/api/v2/calculator/division"
