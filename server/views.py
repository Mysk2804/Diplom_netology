from django.shortcuts import render
from rest_framework.views import APIView
from server.models import User, Category, Shop, ProductInfo, Product, ProductParameter, OrderItem, Order, Contact
from server.serializers import OrderSerializer, ContactSerializer, ProductSerializer, ProductInfoSerializer, \
    ProductParameterSerializer, OrderItemSerializer, UserSerializer


