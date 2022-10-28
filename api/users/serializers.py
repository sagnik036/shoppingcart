from rest_framework import serializers
from .models import *

class UserSerializers(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = [
            'first_name',
            'last_name',
            'username',
            'password',
            'mobile',
            'email',
            'company_name',
            'user_type',
        ]