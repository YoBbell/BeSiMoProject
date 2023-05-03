# Generated by Django 4.2 on 2023-04-29 04:20

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("accounts", "0007_product"),
    ]

    operations = [
        migrations.AddField(
            model_name="product",
            name="collection",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.PROTECT,
                to="accounts.category",
            ),
        ),
    ]
