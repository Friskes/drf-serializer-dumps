from rest_framework import serializers

from tests.models import Person


class PersonCars(serializers.Serializer):
    car_name = serializers.CharField()
    car_price = serializers.IntegerField()


class PersonSerializer1(serializers.Serializer):
    name = serializers.CharField()
    age = serializers.IntegerField()
    cars = PersonCars(many=True)


class PersonSerializer2(serializers.ModelSerializer):
    class Meta:
        model = Person
        fields = '__all__'
