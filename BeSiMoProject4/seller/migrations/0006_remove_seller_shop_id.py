# Generated by Django 3.1.7 on 2023-05-05 17:12

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('seller', '0005_seller_shop_id'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='seller',
            name='shop_id',
        ),
    ]
