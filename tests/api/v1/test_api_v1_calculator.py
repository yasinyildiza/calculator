import typing

import pytest


class BaseOperatorTest:
    name: str = ""
    symbol: str = ""
    endpoint: str = ""

    @pytest.mark.parametrize(
        "json",
        [
            None,
            {},
            {
                "left": 0,
            },
            {
                "right": 0,
            },
            {
                "left": 0,
                "right": "a",
            },
            {
                "left": "a",
                "right": 0,
            },
        ],
    )
    def test_invalid_input_returns_400(self, test_client, json):
        response = test_client.post(self.endpoint, json=json)

        assert response.status_code == 400

    @pytest.fixture
    def values_set(self) -> typing.List[typing.Tuple[int, int, int, str]]:
        """Return a list of Tuples as fixture values for tests.

        [0] -> left
        [1] -> right
        [2] -> result
        [3] -> expression
        """

    def test_valid_input_returns_200(self, test_client, values_set):
        for values in values_set:
            left, right, result, expression = values

            response = test_client.post(
                self.endpoint,
                json={
                    "left": left,
                    "right": right,
                },
            )

            assert response.status_code == 200
            assert response.json == {
                "operands": {
                    "left": left,
                    "right": right,
                },
                "name": self.name,
                "symbol": self.symbol,
                "result": result,
                "expression": expression,
            }


class TestAdd(BaseOperatorTest):
    name = "addition"
    symbol = "+"
    endpoint = "/api/v1/calculator/addition"

    @pytest.fixture
    def values_set(self):
        yield [
            (1, 2, 3, "1 + 2 = 3"),
            (-1, 2, 1, "(-1) + 2 = 1"),
            (1, -2, -1, "1 + (-2) = -1"),
            (-1, -2, -3, "(-1) + (-2) = -3"),
        ]


class TestSubtract(BaseOperatorTest):
    name = "subtraction"
    symbol = "-"
    endpoint = "/api/v1/calculator/subtraction"

    @pytest.fixture
    def values_set(self):
        yield [
            (1, 2, -1, "1 - 2 = -1"),
            (-1, 2, -3, "(-1) - 2 = -3"),
            (1, -2, 3, "1 - (-2) = 3"),
            (-1, -2, 1, "(-1) - (-2) = 1"),
        ]


class TestMultiply(BaseOperatorTest):
    name = "multiplication"
    symbol = "*"
    endpoint = "/api/v1/calculator/multiplication"

    @pytest.fixture
    def values_set(self):
        yield [
            (1, 2, 2, "1 * 2 = 2"),
            (-1, 2, -2, "(-1) * 2 = -2"),
            (1, -2, -2, "1 * (-2) = -2"),
            (-1, -2, 2, "(-1) * (-2) = 2"),
        ]


class TestDivide(BaseOperatorTest):
    name = "division"
    symbol = "//"
    endpoint = "/api/v1/calculator/division"

    @pytest.fixture
    def values_set(self):
        yield [
            (14, 7, 2, "14 // 7 = 2"),
            (-18, 6, -3, "(-18) // 6 = -3"),
            (17, -2, -9, "17 // (-2) = -9"),
            (-24, -4, 6, "(-24) // (-4) = 6"),
        ]
