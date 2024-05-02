from time import sleep
from unittest.mock import ANY

from src.drf_serializer_dumps.decorators import serializer_dumps

from tests.serializers import PersonSerializer1, PersonSerializer2


# python -m pip install .
# pytest -s ./tests
def test_serializer_dumps() -> None:
    """"""
    result = serializer_dumps(PersonSerializer1, exclude_fields=['age'])
    assert result == {
        'name': 'string',
        'birthday': ANY,
        'field_without_annotation': None,
        'height': 1,
        'weight': 1,
        'cars': [{'car_name': 'string', 'car_price': 1}],
        'house': {'address': 'string'},
    }


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
        'house': {'address': 'string'},
    }

    result1 = serializer_dumps(PersonSerializer1, renew_type_value=True)
    assert result1 == expected

    sleep(0.01)

    result2 = serializer_dumps(PersonSerializer1, renew_type_value=True)
    assert result2 == expected

    assert result1['birthday'] != result2['birthday']
