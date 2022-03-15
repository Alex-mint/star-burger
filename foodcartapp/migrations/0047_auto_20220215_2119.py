# Generated by Django 3.2 on 2022-02-15 20:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('foodcartapp', '0046_alter_orderproduct_product_price'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='comment',
            field=models.TextField(blank=True, verbose_name='Комментарий к заказу'),
        ),
        migrations.AlterField(
            model_name='order',
            name='status',
            field=models.CharField(choices=[('handled', 'Обработанный'), ('unhandled', 'Необработанный')], db_index=True, default='unhandled', max_length=20, verbose_name='Статус заказа'),
        ),
    ]