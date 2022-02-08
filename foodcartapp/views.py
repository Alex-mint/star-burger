import json

from django.http import JsonResponse
from django.templatetags.static import static
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from .models import Product, Order, OrderProduct


def banners_list_api(request):
    # FIXME move data to db?
    return JsonResponse([
        {
            'title': 'Burger',
            'src': static('burger.jpg'),
            'text': 'Tasty Burger at your door step',
        },
        {
            'title': 'Spices',
            'src': static('food.jpg'),
            'text': 'All Cuisines',
        },
        {
            'title': 'New York',
            'src': static('tasty.jpg'),
            'text': 'Food is incomplete without a tasty dessert',
        }
    ], safe=False, json_dumps_params={
        'ensure_ascii': False,
        'indent': 4,
    })


def product_list_api(request):
    products = Product.objects.select_related('category').available()

    dumped_products = []
    for product in products:
        dumped_product = {
            'id': product.id,
            'name': product.name,
            'price': product.price,
            'special_status': product.special_status,
            'description': product.description,
            'category': {
                'id': product.category.id,
                'name': product.category.name,
            },
            'image': product.image.url,
            'restaurant': {
                'id': product.id,
                'name': product.name,
            }
        }
        dumped_products.append(dumped_product)
    return JsonResponse(dumped_products, safe=False, json_dumps_params={
        'ensure_ascii': False,
        'indent': 4,
    })


@api_view(['POST'])
def register_order(request):
    response = request.data
    order = Order.objects.create(
        firstname=response['firstname'],
        lastname=response['lastname'],
        phone=response['phonenumber'],
        address=response['address'],
    )
    try:
        products = response['products']
    except:
        content = {'error': 'products: Обязательное поле.'}
        return Response(content, status=status.HTTP_404_NOT_FOUND)
    if isinstance(products, str):
        content = {'error': 'products: Ожидался list со значениями, но был получен "str".'}
        return Response(content, status=status.HTTP_404_NOT_FOUND)
    if (products is None) or not products:
        content = {'error': 'products: Этот список не может быть пустым.'}
        return Response(content, status=status.HTTP_404_NOT_FOUND)
    else:
        for item in response['products']:
            try:
                product = Product.objects.get(pk=item['product'])
            except TypeError:
                raise
            OrderProduct.objects.create(
                order=order,
                product=product,
                quantity=item['quantity'])
        return Response({})

