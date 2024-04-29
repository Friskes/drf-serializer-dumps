# Decorator for creating dict based on the drf serializer class for swagger

<div align="center">

| Project   |     | Status                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                        |
|-----------|:----|-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| CI/CD     |     | [![Latest Release](https://github.com/Friskes/drf-serializer-dumps/actions/workflows/publish-to-pypi.yml/badge.svg)](https://github.com/Friskes/drf-serializer-dumps/actions/workflows/publish-to-pypi.yml)                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                             |
| Quality   |     | [![Coverage](https://codecov.io/github/Friskes/drf-serializer-dumps/graph/badge.svg?token=vKez4Pycrc)](https://codecov.io/github/Friskes/drf-serializer-dumps)                                                                                                                                                                                                                                                                                                                               |
| Package   |     | [![PyPI - Version](https://img.shields.io/pypi/v/drf-serializer-dumps?labelColor=202235&color=edb641&logo=python&logoColor=edb641)](https://badge.fury.io/py/drf-serializer-dumps) ![PyPI - Support Python Versions](https://img.shields.io/pypi/pyversions/drf-serializer-dumps?labelColor=202235&color=edb641&logo=python&logoColor=edb641) ![Project PyPI - Downloads](https://img.shields.io/pypi/dm/drf-serializer-dumps?logo=python&label=downloads&labelColor=202235&color=edb641&logoColor=edb641)                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                  |
| Meta      |     | [![types - Mypy](https://img.shields.io/badge/types-Mypy-202235.svg?logo=python&labelColor=202235&color=edb641&logoColor=edb641)](https://github.com/python/mypy) [![License - MIT](https://img.shields.io/badge/license-MIT-202235.svg?logo=python&labelColor=202235&color=edb641&logoColor=edb641)](https://spdx.org/licenses/) [![code style - Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/format.json&labelColor=202235)](https://github.com/astral-sh/ruff) |

</div>

> Provides a decorator for converting the drf serializer class to a dictionary

## Install
1. Install package
    ```bash
    pip install drf-serializer-dumps
    ```

## About decorator
`serializer_dumps` decorator is based on the assignment of fields in the serializer to generate a dict, for `SerializerMethodField`, the definition is made by `OpenApiTypes` or the usual python type hints.

- Optional parameters:
    - `exclude_fields` Exclude a number of serializer fields when generating a dictionary.
    - `renew_type_value` Generate a new `uuid` and `datetime, date, time` when calling the function.
    - `extend_type_map` Expand the type dictionary to default values, new types and their values, or redefine existing types and their values.

## Usage example

### Example 1
```python
from rest_framework import serializers
from drf_serializer_dumps.decorators import serializer_dumps


class PersonCars(serializers.Serializer):
    car_name = serializers.CharField()
    car_price = serializers.IntegerField()


class PersonSerializer(serializers.Serializer):
    name = serializers.CharField()
    age = serializers.IntegerField()
    cars = PersonCars(many=True)


result = serializer_dumps(PersonSerializer)
print(result)
>>> {'name': 'string', 'age': 1, 'cars': [{'car_name': 'string', 'car_price': 1}]}
```

### Example 2
```python
from rest_framework import serializers
from django.contrib.postgres.fields import ArrayField
from drf_serializer_dumps.decorators import serializer_dumps


class Person(models.Model):
    name = models.CharField(max_length=256)
    phones = ArrayField(models.CharField(max_length=256))


class PersonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Person
        fields = '__all__'


result = serializer_dumps(PersonSerializer)
print(result)
>>> {'id': 1, 'name': 'string', 'phones': ['string']}
```

### Example 3
> Integration with drf-spectacular extend_schema decorator
```python
@extend_schema(
    examples=[
        OpenApiExample('Name1', serializer_dumps(Some1Serializer)),
        OpenApiExample('Name2', serializer_dumps(Some2Serializer)),
    ]
)
def your_api_method(self, request, *args, **kwargs):
    ...
```

## Contributing
We would love you to contribute to `drf-serializer-dumps`, pull requests are very welcome! Please see [CONTRIBUTING.md](https://github.com/Friskes/drf-serializer-dumps/blob/main/CONTRIBUTING.md) for more information.
