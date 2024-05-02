from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import extend_schema_field
from rest_framework import serializers

from tests.models import Person


class PersonCars(serializers.Serializer):
    car_name = serializers.CharField()
    car_price = serializers.IntegerField()


class PersonHouse(serializers.Serializer):
    address = serializers.CharField()


class PersonSerializer1(serializers.Serializer):
    name = serializers.CharField()
    age = serializers.IntegerField()
    birthday = serializers.DateTimeField()

    field_without_annotation = serializers.SerializerMethodField()

    def get_field_without_annotation(self, obj: object):  # type: ignore[no-untyped-def]
        return 'Hello world!'

    height = serializers.SerializerMethodField()

    def get_height(self, obj: object) -> int:
        return 184

    weight = serializers.SerializerMethodField()

    @extend_schema_field(OpenApiTypes.INT)
    def get_weight(self, obj):  # type: ignore[no-untyped-def]
        return 78

    cars = PersonCars(many=True)

    house = PersonHouse()


class PersonSerializer2(serializers.ModelSerializer):
    class Meta:
        model = Person
        fields = '__all__'
