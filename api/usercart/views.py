from django.shortcuts import render
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import GenericAPIView
from rest_framework import status
from .models import *
from .info import *
from rest_framework.response import Response
from .serializers import *
from django.db.models import Q
from api.common.errors import *
# Create your views here.

class UserCartViews(GenericAPIView):
    serializer_class = UserCartSerializers
    queryset = ''
    authentication_classes=[JWTAuthentication]
    permission_classes = [IsAuthenticated]

    @classmethod
    def get(cls, request):
        user = request.user
        instance = UserCart.objects.filter(user=user)
        response = [CartInfo.list_data(i) for i in instance]
        return Response(response, status=status.HTTP_200_OK)
    
    @classmethod
    def post(cls,request):
        user = request.user
        validate_data = UserCartSerializers(data=request.data)
        
        if validate_data.is_valid():
            data = validate_data.validated_data
            products = list(data.get('products').split(','))
            try:
                instance = UserCart.objects.get(user=user)
                response = {
                    "errors" : "already exists"
                }
                return Response(response, status= status.HTTP_400_BAD_REQUEST)
            except:
                instance = UserCart.objects.create(
                    user=user,
                )
                for i in products:
                    try:
                        instance_products = Product.objects.get(id = i)
                        instance.products.add(instance_products)
                    except Exception as e:
                        response ={
                            "error" : f"{e}"
                        }
                        instance.delete()
                        return Response(response, status= status.HTTP_400_BAD_REQUEST)
                response = {
                    "message" :"cart added",
                    "cart-id" : instance.id
                }
                return Response(response,status=status.HTTP_201_CREATED)
        else:
            errors = FormatResponses.error_response(validate_data.errors)
            response = {
                "errors": errors
            }
            return Response(response, status=status.HTTP_400_BAD_REQUEST)
    
    @classmethod
    def put(cls, request):
        data = request.GET
        id = data.get('id')
        user = request.user
        try:
            instance = UserCart.objects.get(id = id)
            serializer = UserCartSerializers(instance, data=request.data)
            if serializer.is_valid():
                data = serializer.validated_data
                products = list(data.get('products').strip().split(','))
                instance.products.clear()
                for i in products:
                    try:
                        instance_products = Product.objects.get(id = i)
                        instance.products.add(instance_products)
                    except Exception as e:
                        response ={
                            "error" : f"{e}"
                        }
                        instance.delete()
                        return Response(response, status= status.HTTP_400_BAD_REQUEST)
                response = {
                    "message" :"cart updated",
                    "cart-id" : instance.id
                }
                return Response(response,status=status.HTTP_201_CREATED)

            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            response = {
                "errors" : f"{e}"
            }
            return Response(response, status=status.HTTP_400_BAD_REQUEST)

    @classmethod
    def delete(self, request):
        data = request.GET
        id = data.get('id')
        user = request.user
        try:
            filter_query=Q(id=id,user=user)
            instance = UserCart.objects.get(filter_query)
            instance.delete()
            response = {
                "message" : "deleted"
            }
            return Response(response, status=status.HTTP_200_OK)
        except Exception as e:
            response = {
                "errors" : f"{e}"
            }
            return Response(response , status=status.HTTP_400_BAD_REQUEST)