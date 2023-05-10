# Generated by Django 4.1.6 on 2023-05-09 10:49

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('seller', '0003_alter_orderitem_payment'),
    ]

    operations = [
        migrations.AddField(
            model_name='seller',
            name='closing_time',
            field=models.TimeField(default=datetime.datetime(2023, 5, 9, 22, 0, 0, 187785, tzinfo=datetime.timezone.utc)),
        ),
        migrations.AddField(
            model_name='seller',
            name='opening_time',
            field=models.TimeField(default=datetime.datetime(2023, 5, 9, 9, 0, 0, 187785, tzinfo=datetime.timezone.utc)),
        ),
    ]