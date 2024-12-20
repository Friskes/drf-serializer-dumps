from __future__ import annotations

import json
from datetime import date, datetime, time, timedelta
from typing import (  # noqa: UP035
    TYPE_CHECKING,
    Any,
    Dict,
    List,
    Set,
    Tuple,
    Union,
    get_args,
    get_origin,
    get_type_hints,
)
from uuid import UUID, uuid4

from django.utils import timezone
from drf_spectacular.types import OpenApiTypes
from rest_framework import serializers

if TYPE_CHECKING:
    from collections import OrderedDict

    from drf_spectacular.utils import _SerializerType

try:
    from types import UnionType  # type: ignore[attr-defined]
except ImportError:
    UnionType = Union

__all__ = ('serializer_dumps',)

_uuid = uuid4()
_now = timezone.now()


def serializer_dumps(
    klass: _SerializerType,
    exclude_fields: list[str] | None = None,
    renew_type_value: bool = False,
    extend_type_map: dict[type, Any] | None = None,
) -> dict[str, Any]:
    """
    - Generates an `Example Value` for `Swagger` based on the serializer class,\
    using field names, field classes, and field types.
    - It also searches for types in the decorator `@extend_schema_field` with `OpenApiTypes` types.
    - If the `SerializerMethodField` method returns a nested serializer,\
    then the class of this serializer must be specified as `type hints`.

    ---

    #### Example 1::

        class PersonCars(serializers.Serializer):
            car_name = serializers.CharField()
            car_price = serializers.IntegerField()

        class PersonSerializer(serializers.Serializer):
            name = serializers.CharField()
            age = serializers.IntegerField()
            cars = PersonCars(many=True)
        -----------------------------------------------
        serializer_dumps(PersonSerializer)
        {'name': 'string', 'age': 1, 'cars': [{'car_name': 'string', 'car_price': 1}]}

    #### Example 2::

        class Person(models.Model):
            name = models.CharField(max_length=256)
            phones = ArrayField(models.CharField(max_length=256))

        class PersonSerializer(serializers.ModelSerializer):
            class Meta:
                model = Person
                fields = '__all__'
        -----------------------------------------------
        serializer_dumps(PersonSerializer)
        {'id': 1, 'name': 'string', 'phones': ['string']}

    ---

    #### Integration with drf-spectacular extend_schema decorator::

        @extend_schema(
            examples=[
                OpenApiExample('Name1', serializer_dumps(Some1Serializer)),
                OpenApiExample('Name2', serializer_dumps(Some2Serializer)),
            ]
        )
        def your_api_method(self, request, *args, **kwargs):
            ...

    - Optional parameters:
        - `exclude_fields` Exclude a number of serializer fields when generating a dictionary.
        - `renew_type_value` Generate a new `uuid` and `datetime, date, time` when calling the function.
        - `extend_type_map` Expand the type dictionary to the default values,\
        with new types and their values, or redefine existing types and their values.
    """
    if exclude_fields is None:
        exclude_fields = []
    if extend_type_map is None:
        extend_type_map = {}

    if renew_type_value:
        global _uuid
        global _now
        _uuid = uuid4()
        _now = timezone.now()

    field_type_mapping = {
        serializers.ChoiceField: 'string',
        serializers.CharField: 'string',
        serializers.FloatField: 1.0,
        serializers.BooleanField: False,
        serializers.IntegerField: 1,
        serializers.UUIDField: _uuid,
        serializers.DateTimeField: _now,
        serializers.DateField: _now.date(),
        serializers.TimeField: _now.time(),
        serializers.DurationField: timedelta(seconds=5),
    }
    reversed_field_type_mapping = {value: field for field, value in field_type_mapping.items()}
    type_mapping = {
        **field_type_mapping,
        OpenApiTypes.STR: 'string',
        OpenApiTypes.DOUBLE: 1.0,
        OpenApiTypes.BOOL: False,
        OpenApiTypes.BINARY: b'string',
        OpenApiTypes.INT: 1,
        OpenApiTypes.UUID: _uuid,
        OpenApiTypes.DATETIME: _now,
        OpenApiTypes.DATE: _now.date(),
        OpenApiTypes.TIME: _now.time(),
        OpenApiTypes.DURATION: timedelta(seconds=5),
        OpenApiTypes.OBJECT: {},
        OpenApiTypes.ANY: {},
        OpenApiTypes.NONE: None,
        str: 'string',
        float: 1.0,
        bool: False,
        bytes: b'string',
        int: 1,
        UUID: _uuid,
        datetime: _now,
        date: _now.date(),
        time: _now.time(),
        timedelta: timedelta(seconds=5),
        dict: {},
        Dict: {},  # noqa: UP006
        Any: {},
        None: None,
        **extend_type_map,
    }
    many_annotations = (list, tuple, set, List, Tuple, Set)  # noqa: UP006

    def _get_type_value(
        klass: _SerializerType,
        field_name: str,
        field_instance: serializers.SerializerMethodField,
    ) -> tuple[Any, Any]:
        """
        Get typing from the SerializerMethodField method
        """
        if field_instance.method_name is None:
            method = getattr(klass, f'get_{field_name}')
        else:
            method = getattr(klass, field_instance.method_name)

        open_api_type = getattr(method, '_spectacular_annotation', {}).get('field')

        # annotation = inspect.signature(method).return_annotation
        # annotation = None if annotation is inspect._empty else annotation

        annotation = get_type_hints(method).get('return')

        # origin = get_origin(annotation)
        # if origin is Union or origin is UnionType:
        if get_origin(annotation) in (Union, UnionType):
            annotation = get_args(annotation)[0]

        type_value = type_mapping.get(open_api_type)
        if type_value is None:
            type_value = type_mapping.get(annotation)

        return type_value, annotation

    def _walk_fields_recursively(
        klass: _SerializerType, exclude_fields: list[str] | None = None
    ) -> dict[str, Any]:
        """
        Recursively walks all fields and nested serializers
        to generate an `Example Value'.
        """
        if exclude_fields is None:
            exclude_fields = []

        fields: OrderedDict[str, _SerializerType] = klass().get_fields()
        example_val: dict[str, Any] = {}

        for field_name, field_instance in fields.items():
            if field_name in exclude_fields:
                continue

            if isinstance(field_instance, serializers.ListSerializer):
                nested_dict = _walk_fields_recursively(type(field_instance.child), exclude_fields)
                example_val[field_name] = [nested_dict] if field_instance.many else nested_dict

            elif isinstance(field_instance, serializers.ListField):  # support for postgres ArrayField
                example_val[field_name] = [type_mapping.get(type(field_instance.child))]

            elif not isinstance(field_instance, serializers.SerializerMethodField):
                base_field_cls = type(field_instance).__bases__[0]  # __mro__
                if base_field_cls is not serializers.Field and not issubclass(
                    base_field_cls, serializers.Serializer
                ):
                    kwargs = {}
                    if isinstance(field_instance, serializers.ChoiceField):
                        kwargs.update({'choices': ()})

                    example_val[field_name] = base_field_cls(**kwargs).to_representation(
                        type_mapping.get(base_field_cls)
                    )
                elif isinstance(field_instance, serializers.Serializer):
                    example_val[field_name] = _walk_fields_recursively(
                        type(field_instance), exclude_fields
                    )
                else:
                    example_val[field_name] = field_instance.to_representation(
                        type_mapping.get(type(field_instance))
                    )

            elif isinstance(field_instance, serializers.SerializerMethodField):
                type_value, annotation = _get_type_value(klass, field_name, field_instance)

                if type_value is not None:
                    _field_instance = reversed_field_type_mapping.get(type_value)

                    if _field_instance is not None:
                        example_val[field_name] = _field_instance().to_representation(type_value)
                    else:
                        example_val[field_name] = type_value
                        print(
                            f'An unknown annotation was found: "{annotation.__name__}" '
                            f'by the field: "{field_name}".'
                        )
                else:
                    # support for: -> list[Serializer] or -> List[Serializer]
                    if annotation is not None and get_origin(annotation) in many_annotations:
                        nested_dict = _walk_fields_recursively(get_args(annotation)[0], exclude_fields)
                        example_val[field_name] = [nested_dict]

                    elif annotation is not None and issubclass(annotation, serializers.Serializer):
                        example_val[field_name] = _walk_fields_recursively(annotation, exclude_fields)
                    else:
                        example_val[field_name] = None
                        print(
                            f'An unknown annotation was found: "{type(annotation).__name__}" '
                            f'For the field: "{field_name}" the value has been set "None".'
                        )
            else:
                example_val[field_name] = None
                print(
                    f'An unknown field has been detected: "{type(field_instance).__name__}" '
                    f'For the field: "{field_name}" the value has been set "None".'
                )

        return example_val

    return json.loads(
        json.dumps(
            _walk_fields_recursively(klass, exclude_fields), ensure_ascii=False, default=str, indent=4
        )
    )
