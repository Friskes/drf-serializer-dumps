import sys
from time import sleep
from unittest.mock import ANY

from src.drf_serializer_dumps.decorators import serializer_dumps

from tests.serializers import PersonSerializer1, PersonSerializer2


# python -m pip install .
# pytest -s ./tests
def test_serializer_dumps() -> None:
    """"""
    result = serializer_dumps(PersonSerializer1, exclude_fields=['age'])
    expected = {
        'name': 'string',
        'birthday': ANY,
        'field_without_annotation': None,
        'height': 1,
        'weight': 1,
        'cars': [{'car_name': 'string', 'car_price': 1}],
        'cars2': [{'car_name': 'string', 'car_price': 1}],
        'house': {'address': 'string', 'cfield': 'string'},
    }
    if sys.version_info >= (3, 9):  # noqa: UP036
        expected.update({'cars3': [{'car_name': 'string', 'car_price': 1}]})

    assert result == expected


def test_model_serializer_dumps() -> None:
    """"""
    result = serializer_dumps(PersonSerializer2)
    assert result == {'id': 1, 'name': 'string', 'phones': ['string']}


def test_renew_type_value() -> None:
    """"""
    expected = {
        'name': 'string',
        'age': 1,
        'birthday': ANY,
        'field_without_annotation': None,
        'height': 1,
        'weight': 1,
        'cars': [{'car_name': 'string', 'car_price': 1}],
        'cars2': [{'car_name': 'string', 'car_price': 1}],
        'house': {'address': 'string', 'cfield': 'string'},
    }
    if sys.version_info >= (3, 9):  # noqa: UP036
        expected.update({'cars3': [{'car_name': 'string', 'car_price': 1}]})

    result1 = serializer_dumps(PersonSerializer1, renew_type_value=True)
    assert result1 == expected

    sleep(0.01)

    result2 = serializer_dumps(PersonSerializer1, renew_type_value=True)
    assert result2 == expected

    assert result1['birthday'] != result2['birthday']
