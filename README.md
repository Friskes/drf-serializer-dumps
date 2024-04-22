# Decorator for creating dict based on the drf serializer class for swagger


> Provides a decorator for converting the drf serializer class to a dictionary


## Requirements
- django>=4.2.11
- djangorestframework>=3.14.0
- drf-spectacular>=0.27.2


## Install
1. `pip install drf-serializer-dumps`


## About decorator
drf_serializer_dumps `serializer_dumps` is based on the assignment of fields in the serializer to generate a dict, for `SerializerMethodField`, the definition is made by `OpenApiTypes` or the usual python type hints.

- Optional parameters:
    - `exclude_fields` Exclude a number of serializer fields when generating a dictionary.
    - `renew_type_value` Generate a new `uuid` and `datetime, date, time` when calling the function.
    - `extend_type_map` Expand the type dictionary to default values, new types and their values, or redefine existing types and their values.


## Usage example

Direct usage

```python
# Example 1
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


# Example 2
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
>>> {'name': 'string', 'phones': ['string']}


# Integration with drf-spectacular extend_schema decorator

    @extend_schema(
        examples=[
            OpenApiExample('Name1', serializer_dumps(Some1Serializer)),
            OpenApiExample('Name2', serializer_dumps(Some2Serializer)),
        ]
    )
    def your_api_method(self, request, *args, **kwargs):
        ...
```
