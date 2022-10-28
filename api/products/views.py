from django.shortcuts import render
from rest_framework.generics import GenericAPIView
from rest_framework import status
from .serializers import *
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from .info import *
from django.db.models import Q
from api.common.errors import *
from rest_framework.response import Response
# Create your views here.

class ProductViews(GenericAPIView):
    serializer_class = ProductSerializers
    queryset=''

    """an api that will list all the products for all the users"""
    @classmethod
    def get(cls, request):
        data = request.GET
        search = data.get('search')
        id = data.get('id')
        filter_query = Q()
        filter_query = Q(is_available=True)
        if id:
            filter_query = Q(
                id = id,
            )
        if search:
            filter_query.add(
                Q(name__startswith=search),
                Q.AND
            )

        product_instances = Product.objects.filter(filter_query)
        print(product_instances)
        response = [ProductsInfo.list_data(i,request) for i in product_instances]
        return Response(response, status=status.HTTP_200_OK)

class SellerProductView(GenericAPIView):
    serializer_class = ProductSerializers
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    queryset=''

    """an api that will fetch all the products listed by a particular seller"""
    @classmethod
    def get(cls, request):
        data = request.GET
        seller = request.user
        search = data.get('search')
        id = data.get('id')
        filter_query = Q(seller=seller)
        if id:
            filter_query = Q(
                id = id,
                seller=seller
            )
        if search:
            filter_query.add(
                Q(name__startswith=search , seller=seller),
                Q.AND
            )

        product_instances = Product.objects.filter(filter_query)
        response = [ProductsInfo.list_data(i,request) for i in product_instances]
        return Response(response, status=status.HTTP_200_OK)

    """an api that will add products for authenticated seller only"""
    @classmethod
    def post(cls, request):
        validate_data = ProductSerializers(data=request.data)
        seller = request.user
        user_type = seller.user_type
        print(user_type)
        if (int(user_type) == 1):
            if validate_data.is_valid():
                data = validate_data.validated_data
                try:
                    instance = Product.objects.create(
                        seller = seller,
                        image = data.get('image'),
                        name = data.get('name'),
                        short_describtion = data.get('short_describtion'),
                        describtion = data.get('describtion'),
                        price = data.get('price'),
                        discount = data.get('discount'),
                        is_available = data.get('is_is_available')
                    )
                    response = {
                        "message" : "added successfully",
                        "id" : instance.id
                    }
                    return Response(response, status= status.HTTP_201_CREATED)
                except Exception as e:
                    response = {
                        "errors" : f"{e}"
                    }
                    return Response(response,status=status.HTTP_400_BAD_REQUEST)
            else:
                errors = FormatResponses.error_response(validate_data.errors)
                response = {
                    "errors": errors
                }
                return Response(response, status=status.HTTP_400_BAD_REQUEST)
        else:
            response={
                "errors" : "you are not seller"
            }
            return Response(response, status=status.HTTP_400_BAD_REQUEST)
            
    @classmethod
    def put(cls, request):
        data = request.GET
        id = data.get('id')
        try:
            instance = Product.objects.get(id = id)
            serializer = ProductSerializers(instance, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
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
        seller = request.user
        try:
            filter_query=Q(id=id,seller=seller)
            instance = Product.objects.get(filter_query)
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


