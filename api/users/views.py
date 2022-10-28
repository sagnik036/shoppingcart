from django.shortcuts import render
from .serializers import *
from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from api.common.errors import *
# Create your views here.

class UserRegistration(GenericAPIView):
    serializer_class = UserSerializers
    queryset = ''

    @classmethod
    def post(cls, request):
        validate_data = UserSerializers(data = request.data)

        if validate_data.is_valid():
            data = validate_data.validated_data
            try:
                user = CustomUser.objects.get(username = data.get('username'))
            except:
                user = None
            
            if user is None:
                try:
                    user_instance = CustomUser.objects.create(
                        username = data.get('username'),
                        password = make_password(data.get('password')),
                        email = data.get('email'),
                        mobile = data.get('mobile'),
                        company_name = data.get('company_name'),
                        user_type = data.get('user_type')
                    )
                    access_token = RefreshToken.for_user(user_instance)
                    response = {
                        "message" : "user_added",
                        "token" : str(access_token.access_token)
                    }
                    return Response(response, status=status.HTTP_201_CREATED)
                except Exception as e:
                    response = {
                        "errors" : f"{e}"
                    }
                    return Response(response, status=status.HTTP_400_BAD_REQUEST)

            else:
                response = {
                    "errors" : "user with username already exists"
                }
                return Response(response, status=status.HTTP_400_BAD_REQUEST)
        else:
            errors = FormatResponses.error_response(validate_data.errors)
            response = {
                "errors": errors
            }
            return Response(response, status=status.HTTP_400_BAD_REQUEST)

