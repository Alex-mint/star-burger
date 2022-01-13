# Generated by Django 3.2 on 2022-01-13 06:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('foodcartapp', '0039_auto_20220112_2251'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='product',
        ),
        migrations.AddField(
            model_name='order',
            name='product',
            field=models.ManyToManyField(related_name='order_items', to='foodcartapp.Product', verbose_name='продукт'),
        ),
    ]