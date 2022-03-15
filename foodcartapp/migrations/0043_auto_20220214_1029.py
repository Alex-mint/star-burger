# Generated by Django 3.2 on 2022-02-14 09:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('foodcartapp', '0042_auto_20220113_1037'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='status',
            field=models.CharField(choices=[('handled', 'Обработанный заказ'), ('unhandled', 'Не обработанный заказ')], db_index=True, default='unhandled', max_length=20, verbose_name='Статус заказа'),
        ),
        migrations.AlterField(
            model_name='order',
            name='phone',
            field=models.CharField(db_index=True, max_length=250, verbose_name='Телефон'),
        ),
    ]