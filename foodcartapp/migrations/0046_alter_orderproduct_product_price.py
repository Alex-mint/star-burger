# Generated by Django 3.2 on 2022-02-14 20:40

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('foodcartapp', '0045_orderproduct_product_price'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orderproduct',
            name='product_price',
            field=models.DecimalField(decimal_places=2, max_digits=8, validators=[django.core.validators.MinValueValidator(0)], verbose_name='Цена товара'),
        ),
    ]
