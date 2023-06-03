from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from rest_framework import serializers
from .models import Product
from rest_framework.decorators import api_view,permission_classes
from rest_framework.response import Response
# from rest_framework import generics
from api.models import Product

from rest_framework.views import APIView
# from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework import status
# from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
# from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.permissions import IsAuthenticated


# from api.views import ProductSerializer

# Create your views here.

# ___________________________________________________________________________________________________
# using api api_view

def index(req):
    return JsonResponse('hello', safe=False)

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'
    def create(self, validated_data):
        return Product.objects.create(**validated_data)

def myProducts(req):
    all_products = ProductSerializer(Product.objects.all(), many=True).data
    return JsonResponse(all_products, safe=False)

@api_view(['GET','POST','DELETE','PUT','PATCH'])
def produc(req,id=-1):
    if req.method =='GET':
        if id > -1:
            try:
                temp_product=Product.objects.get(id=id)
                return Response (ProductSerializer(temp_product,many=False).data)
            except Product.DoesNotExist:
                return Response ("not found")
        all_products=ProductSerializer(Product.objects.all(),many=True).data
        return Response ( all_products)
    if req.method =='POST':
        pd_serializer = ProductSerializer(data=req.data)
        if pd_serializer.is_valid():
            pd_serializer.save()
            return Response ("post...")
        else:
            return Response (pd_serializer.errors)
    if req.method =='DELETE':
        try:
            temp_product=Product.objects.get(id=id)
        except Product.DoesNotExist:
            return Response ("not found")    
       
        temp_product.delete()
        return Response ("del...")
    if req.method =='PUT':
        try:
            temp_product=Product.objects.get(id=id)
        except Product.DoesNotExist:
            return Response ("not found")
       
        ser = ProductSerializer(data=req.data)
        old_product = Product.objects.get(id=id)
        res = ser.update(old_product, req.data)
        return Response(res)
    


# ___________________________________________________________________________________________________

@permission_classes([IsAuthenticated])
class MyModelView(APIView):
    """
    This class handle the CRUD operations for MyModel
    """
    def get(self, request):
        """
        Handle GET requests to return a list of MyModel objects
        """
        my_model = Product.objects.all()
        serializer = ProductSerializer(my_model, many=True)
        return Response(serializer.data)


    def post(self, request):
        """
        Handle POST requests to create a new Product object
        """
        # usr =request.user
        # print(usr)
        serializer = ProductSerializer(data=request.data, context={'user': request.user})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
   
    def put(self, request, pk):
        """
        Handle PUT requests to update an existing Product object
        """
        my_model = Product.objects.get(pk=pk)
        serializer = ProductSerializer(my_model, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
   
    def delete(self, request, pk):
        """
        Handle DELETE requests to delete a Product object
        """
        my_model = Product.objects.get(pk=pk)
        my_model.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)