from src.drf_serializer_dumps.decorators import serializer_dumps

from tests.serializers import PersonSerializer1, PersonSerializer2


# python -m pip install .
# pytest -s ./tests
def test_serializer_dumps() -> None:
    """"""
    result = serializer_dumps(PersonSerializer1)
    assert result == {'name': 'string', 'age': 1, 'cars': [{'car_name': 'string', 'car_price': 1}]}


def test_model_serializer_dumps() -> None:
    """"""
    result = serializer_dumps(PersonSerializer2)
    assert result == {'id': 1, 'name': 'string', 'phones': ['string']}
