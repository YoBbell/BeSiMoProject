# Generated by Django 4.2 on 2023-04-30 02:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("accounts", "0012_alter_product_image_alter_product_inventory"),
    ]

    operations = [
        migrations.AddField(
            model_name="product",
            name="location",
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name="product",
            name="image",
            field=models.ImageField(blank=True, null=True, upload_to=""),
        ),
    ]