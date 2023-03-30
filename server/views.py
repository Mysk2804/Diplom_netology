from django.shortcuts import render
from django.http import JsonResponse
from rest_framework.generics import ListAPIView
from requests import get
import os
from django.core.exceptions import ValidationError
from django.core.validators import URLValidator
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate
import yaml
from yaml.loader import SafeLoader
# from django.contrib.auth.password_validation import validate_password
from server.models import User, Category, Shop, ProductInfo, Product, ProductParameter, OrderItem, Order, Contact,\
    Parameter
from server.serializers import OrderSerializer, ContactSerializer, ProductSerializer, ProductInfoSerializer, \
    ProductParameterSerializer, OrderItemSerializer, UserSerializer
from pprint import pprint


class RegisterAccount(APIView):
    """
    Для регистрации покупателей
    """
    # Регистрация методом POST
    def post(self, request, *args, **kwargs):

        # проверяем обязательные аргументы
        if {'first_name', 'last_name', 'email', 'password', 'type', 'username'}.issubset(request.data):
            errors = {}

            # проверяем данные для уникальности имени пользователя
            request.data.update({})
            user_serializer = UserSerializer(data=request.data)
            if user_serializer.is_valid():
                # сохраняем пользователя
                user = user_serializer.save()
                user.set_password(request.data['password'])
                user.save()
                return JsonResponse({'Status': True})
            else:
                return JsonResponse({'Status': False, 'Errors': user_serializer.errors})

        return JsonResponse({'Status': False, 'Errors': 'Не указаны все необходимые аргументы'})


class LoginAccount(APIView):
    """
    Класс для авторизации пользователей
    """
    # Авторизация методом POST
    def post(self, request, *args, **kwargs):

        if {'email', 'password'}.issubset(request.data):
            user = authenticate(request, username=request.data['email'], password=request.data['password'])

            if user is not None:
                if user.is_active:
                    token, _ = Token.objects.get_or_create(user=user)

                    return JsonResponse({'Status': True, 'Token': token.key})

            return JsonResponse({'Status': False, 'Errors': 'Не удалось авторизовать'})

        return JsonResponse({'Status': False, 'Errors': 'Не указаны все необходимые аргументы'})


class AccountDetails(APIView):
    """
    Класс для работы данными пользователя
    """

    # получить данные
    def get(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return JsonResponse({'Status': False, 'Error': 'Log in required'}, status=403)

        serializer = UserSerializer(request.user)
        return Response(serializer.data)


class PartnerUpdate(APIView):
    """
    Класс для обновления прайса от поставщика
    """
    def post(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return JsonResponse({'Status': False, 'Error': 'Log in required'}, status=403)

        if request.user.type != 'seller':
            return JsonResponse({'Status': False, 'Error': 'Только для магазинов'}, status=403)

        url = request.data.get('url')
        if url:
            validate_url = URLValidator()
            try:
                validate_url(url)
            except ValidationError as e:
                return JsonResponse({'Status': False, 'Error': str(e)})
            else:
                stream = os.path.join(os.getcwd(), 'shop1.yaml')
                # stream = get(url).content

                with open(stream, encoding='UTF-8') as f:
                    # читаем документ YAML
                    data = yaml.load(f, Loader=SafeLoader)
                    pprint(data)

                    shop, _ = Shop.objects.get_or_create(name=data['shop'], user_id=request.auth.user.id)
                    for category in data['categories']:
                        category_object, _ = Category.objects.get_or_create(id=category['id'], name=category['name'])
                        category_object.shops.add(shop.id)
                        category_object.save()
                    ProductInfo.objects.filter(shop_id=shop.id).delete()
                    for item in data['goods']:
                        product, _ = Product.objects.get_or_create(name=item['name'], category_id=item['category'])

                        product_info = ProductInfo.objects.create(product_id=product.id,
                                                                  model=item['model'],
                                                                  price=item['price'],
                                                                  price_rrc=item['price_rrc'],
                                                                  quantity=item['quantity'],
                                                                  shop_id=shop.id)
                        for name, value in item['parameters'].items():
                            parameter_object, _ = Parameter.objects.get_or_create(name=name)
                            ProductParameter.objects.create(product_info_id=product_info.id,
                                                            parameter_id=parameter_object.id,
                                                            value=value)

                    return JsonResponse({'Status': True})

        return JsonResponse({'Status': False, 'Errors': 'Не указаны все необходимые аргументы'})




