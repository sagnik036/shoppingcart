from rest_framework import serializers
from .models import *


class ProductSerializers(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['image', 'name', 'short_describtion',
                  'describtion', 'price', 'discount', 'is_available']
