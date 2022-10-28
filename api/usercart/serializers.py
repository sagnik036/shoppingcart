from rest_framework import serializers
from .models import *

class UserCartSerializers(serializers.Serializer):
    products = serializers.CharField(

        required =True
    )

    @classmethod
    def validate(cls, data):
        errors = {}
        if errors:
            raise serializers.ValidationError(data)
        return super(UserCartSerializers, cls).validate(cls, data)
