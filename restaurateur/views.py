from django import forms
from django.forms import model_to_dict
from django.shortcuts import redirect, render
from django.template.defaultfilters import first
from django.views import View
from django.urls import reverse_lazy
from django.contrib.auth.decorators import user_passes_test

from django.contrib.auth import authenticate, login
from django.contrib.auth import views as auth_views
from collections import Counter

from foodcartapp.models import Product, Restaurant, Order, RestaurantMenuItem, \
    OrderProduct


class Login(forms.Form):
    username = forms.CharField(
        label='Логин', max_length=75, required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Укажите имя пользователя'
        })
    )
    password = forms.CharField(
        label='Пароль', max_length=75, required=True,
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Введите пароль'
        })
    )


class LoginView(View):
    def get(self, request, *args, **kwargs):
        form = Login()
        return render(request, "login.html", context={
            'form': form
        })

    def post(self, request):
        form = Login(request.POST)

        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']

            user = authenticate(request, username=username, password=password)
            if user:
                login(request, user)
                if user.is_staff:  # FIXME replace with specific permission
                    return redirect("restaurateur:RestaurantView")
                return redirect("start_page")

        return render(request, "login.html", context={
            'form': form,
            'ivalid': True,
        })


class LogoutView(auth_views.LogoutView):
    next_page = reverse_lazy('restaurateur:login')


def is_manager(user):
    return user.is_staff  # FIXME replace with specific permission


@user_passes_test(is_manager, login_url='restaurateur:login')
def view_products(request):
    restaurants = list(Restaurant.objects.order_by('name'))
    products = list(Product.objects.prefetch_related('menu_items'))

    default_availability = {restaurant.id: False for restaurant in restaurants}
    products_with_restaurants = []
    for product in products:

        availability = {
            **default_availability,
            **{item.restaurant_id: item.availability for item in product.menu_items.all()},
        }
        orderer_availability = [availability[restaurant.id] for restaurant in restaurants]

        products_with_restaurants.append(
            (product, orderer_availability)
        )

    return render(request, template_name="products_list.html", context={
        'products_with_restaurants': products_with_restaurants,
        'restaurants': restaurants,
    })


@user_passes_test(is_manager, login_url='restaurateur:login')
def view_restaurants(request):
    return render(request, template_name="restaurants_list.html", context={
        'restaurants': Restaurant.objects.all(),
    })


def get_restaurants(order, orders_items, products_by_restaurants):
    products_in_order = [
        item['product'] for item in orders_items if item['order'] == order.id
    ]
    restaurants_by_order = Counter(
        (
            items['restaurant__name']
        ) for items in products_by_restaurants if
        items['product'] in products_in_order
    )
    return [
        first(item) for item in
        restaurants_by_order.most_common(len(products_in_order))
    ]


@user_passes_test(is_manager, login_url='restaurateur:login')
def view_orders(request):
    unhandled_orders = Order.objects.filter(
        status='unhandled').count_price()
    orders_items = OrderProduct.objects.filter(
        order__in=unhandled_orders
    ).values('order', 'product')

    products_by_restaurants = RestaurantMenuItem.objects.filter(
        availability=True, product__in=orders_items.values('product')
    ).values('restaurant__name', 'restaurant__address', 'product')
    orders_details = []
    for order in unhandled_orders:
        restaurants = []
        get_restaurants(order, orders_items, products_by_restaurants)

        for name in get_restaurants(order, orders_items, products_by_restaurants):
            restaurants.append(
                {
                    'name': name,
                }
            )
        order_details = {
            'order': order,
            'restaurants': restaurants,
        }
        print(order_details)
        orders_details.append(order_details)
    return render(request, template_name='order_items.html', context={
        'order_details': orders_details})
