from rest_framework.decorators import api_view,permission_classes
from rest_framework.response import Response
from django.shortcuts import render, get_object_or_404
from ecommerce.models import Products,NewArrival,BestSeller,User
from .serializers import ProductsSerializer,ProductDetailSerializer,NewArrivalSerializer,BestSellerSerializer,CartSerializer
import requests
from django.views.decorators.csrf import csrf_exempt
from rest_framework.permissions import IsAuthenticated


@api_view(['GET'])
def products(request):
    instance = Products.objects.all()
    
    q = request.GET.get("q")
    if q:
        ids = q.split(",")
        instance = instance.filter(category__in=ids)  
    
    context = {
        'request' : request
    }
    
    serializer = ProductsSerializer(instance, context=context, many=True)
    
    response_data = {
        "data": serializer.data,
        "status_code": 6000,
    }
    return Response(response_data)



@api_view(["GET"])
def product(request,pk):
    if Products.objects.filter(pk=pk).exists():
        instance= Products.objects.get(pk=pk)
        
        context = {
        'request' : request
        }
        
        serializer =ProductDetailSerializer(instance,context=context)
        
        response_data ={
        "data" : serializer.data,
        "status_code" : 6000,
       }
    
        return Response(response_data)
    else:
        response_data = {
            "status_code" : 6001,
            "message" : "Product Not Exist"
        }
        return Response(response_data)
        
        
@api_view(['GET'])
def new_arrival(request):
    instance = NewArrival.objects.all()
    
    context = {
        'request' : request
    }
    
    serializers = NewArrivalSerializer(instance, context=context, many=True)
    
    response_data ={
        "data" : serializers.data,
        "status_code" : 6000,
    }
    return Response(response_data)


@api_view(['GET'])
def best_seller(request):
    instance = BestSeller.objects.all()
    
    context = {
        'request' : request
    }
    
    serializers = BestSellerSerializer(instance, context=context, many=True)
    
    response_data ={
        "data" : serializers.data,
        "status_code" : 6000,
    }
    return Response(response_data)



@api_view(["GET"])
@permission_classes([IsAuthenticated])
def cart(request):
    user = request.user
    item = get_object_or_404(User, user=user)
    
    context = {
        "request": request
    }

    serializer = CartSerializer(item.items.all(), many=True, context=context)
    
    response_data = {
        "data":serializer.data,
        "status_code" : 6000
    }
    return Response(response_data)


@api_view(["POST"])
@permission_classes([IsAuthenticated])
@csrf_exempt
def add_cart(request,pk):
    user=request.user
    instance = get_object_or_404(Products, pk=pk)
    
    carts,_= User.objects.get_or_create(user=user)
    carts.items.add(instance)
    carts.save()
    
    serializer = CartSerializer(instance, data=request.data, partial=True)
    
    if serializer.is_valid():
        serializer.save()
        
        response_data ={
            
         "status_code": 200,
        "message": "Added to Cart"
       
        }
        
        return Response(response_data, status=200, content_type='application/json')
    
    return Response({"status_code": 400, "message": "Validation error", "data": serializer.errors})


@csrf_exempt
@api_view(["POST"])
@permission_classes([IsAuthenticated])
def delete_cart_item(request, pk):
    user = request.user
    product_item = get_object_or_404(Products, pk=pk)
    cart = get_object_or_404(User, user=user)
    
    cart.items.remove(product_item)

    response_data = {
        "status_code": 200,
        "message": "Item removed from cart"
    }
    return Response(response_data)