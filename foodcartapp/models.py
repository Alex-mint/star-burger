from django.db import models
from django.core.validators import MinValueValidator
from django.db.models import Sum, F
from django.utils import timezone


class Restaurant(models.Model):
    name = models.CharField(
        'название',
        max_length=50
    )
    address = models.CharField(
        'адрес',
        max_length=100,
        blank=True,
    )
    contact_phone = models.CharField(
        'контактный телефон',
        max_length=50,
        blank=True,
    )

    class Meta:
        verbose_name = 'ресторан'
        verbose_name_plural = 'рестораны'

    def __str__(self):
        return self.name


class ProductQuerySet(models.QuerySet):
    def available(self):
        products = (
            RestaurantMenuItem.objects
            .filter(availability=True)
            .values_list('product')
        )
        return self.filter(pk__in=products)


class ProductCategory(models.Model):
    name = models.CharField(
        'название',
        max_length=50
    )

    class Meta:
        verbose_name = 'категория'
        verbose_name_plural = 'категории'

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(
        'название',
        max_length=50
    )
    category = models.ForeignKey(
        ProductCategory,
        verbose_name='категория',
        related_name='products',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
    )
    price = models.DecimalField(
        'цена',
        max_digits=8,
        decimal_places=2,
        validators=[MinValueValidator(0)]
    )
    image = models.ImageField(
        'картинка'
    )
    special_status = models.BooleanField(
        'спец.предложение',
        default=False,
        db_index=True,
    )
    description = models.TextField(
        'описание',
        max_length=200,
        blank=True,
    )

    objects = ProductQuerySet.as_manager()

    class Meta:
        verbose_name = 'товар'
        verbose_name_plural = 'товары'

    def __str__(self):
        return self.name


class RestaurantMenuItem(models.Model):
    restaurant = models.ForeignKey(
        Restaurant,
        related_name='menu_items',
        verbose_name="ресторан",
        on_delete=models.CASCADE,
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name='menu_items',
        verbose_name='продукт',
    )
    availability = models.BooleanField(
        'в продаже',
        default=True,
        db_index=True
    )

    class Meta:
        verbose_name = 'пункт меню ресторана'
        verbose_name_plural = 'пункты меню ресторана'
        unique_together = [
            ['restaurant', 'product']
        ]

    def __str__(self):
        return f"{self.restaurant.name} - {self.product.name}"


class OrderQuerySet(models.QuerySet):
    def count_price(self):
        total_price = self.annotate(
            total_price=Sum(F('order_products__quantity') * F(
                'order_products__product_price')))
        return total_price


class Order(models.Model):
    HANDLED_ORDER = 'handled'
    NEW_ORDER = 'unhandled'
    STATUS = [
        (HANDLED_ORDER, 'Обработанный'),
        (NEW_ORDER, 'Необработанный'),
    ]
    CASH = 'cash'
    CARD = 'card'
    UNKNOWN = 'unknown'
    PAYMENT_METHOD = [
        (CASH, 'Наличкой'),
        (CARD, 'Картой'),
        (UNKNOWN, 'Неизвестно')
    ]
    address = models.CharField(
        'Aдрес',
        max_length=250
    )
    firstname = models.CharField(
        'Имя',
        max_length=250
    )
    lastname = models.CharField(
        'Фамилия',
        max_length=250
    )
    phonenumber = models.CharField(
        'Телефон',
        max_length=250,
        db_index=True
    )
    registrated_at = models.DateTimeField(
        'Заказ создан',
        db_index=True,
        default=timezone.now
    )
    colled_at = models.DateTimeField(
        'Звонок клиенту',
        db_index=True,
        blank=True,
        null=True
    )
    derivered_at = models.DateTimeField(
        'Заказ доставлен',
        db_index=True,
        blank=True,
        null=True
    )
    payment_method = models.CharField(
        'Способ оплаты',
        choices=PAYMENT_METHOD,
        default=UNKNOWN,
        max_length=12,
        db_index=True
    )
    status = models.CharField(
        'Статус заказа',
        choices=STATUS,
        default=NEW_ORDER,
        max_length=20,
        db_index=True
    )
    restaurant = models.ForeignKey(
        Restaurant,
        related_name='orders',
        on_delete=models.CASCADE,
        verbose_name='ресторан',
        null=True
    )
    comment = models.TextField(
        'Комментарий к заказу',
        blank=True
    )
    objects = OrderQuerySet.as_manager()

    class Meta:
        verbose_name = 'заказ'
        verbose_name_plural = 'заказы'

    def __str__(self):
        return f'{self.firstname} {self.lastname} {self.address}'


class OrderProduct(models.Model):
    order = models.ForeignKey(
        Order, on_delete=models.CASCADE,
        verbose_name='заказ',
        related_name='order_products'
    )
    product = models.ForeignKey(
        Product, on_delete=models.DO_NOTHING,
        verbose_name='продукт',
        related_name='selected_product'
    )
    quantity = models.PositiveIntegerField(
        'количество',
        default=1
    )
    product_price = models.DecimalField(
        'Цена товара',
        max_digits=8,
        decimal_places=2,
        validators=[MinValueValidator(0)],
    )

    def __str__(self):
        return f'{self.order} {self.product}'

    class Meta:
        ordering = ['id']
        verbose_name = 'продукт заказа'
        verbose_name_plural = 'продукты заказа'
