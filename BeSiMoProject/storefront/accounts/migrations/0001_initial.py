# Generated by Django 4.2 on 2023-04-21 10:37

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Buyer",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "first_name",
                    models.CharField(
                        max_length=100,
                        validators=[
                            django.core.validators.RegexValidator(
                                "^[a-zA-Z ]+$", "Only letters and spaces are allowed."
                            )
                        ],
                        verbose_name="First Name",
                    ),
                ),
                (
                    "last_name",
                    models.CharField(
                        max_length=100,
                        validators=[
                            django.core.validators.RegexValidator(
                                "^[a-zA-Z ]+$", "Only letters and spaces are allowed."
                            )
                        ],
                        verbose_name="Last Name",
                    ),
                ),
                (
                    "phone",
                    models.CharField(
                        max_length=10,
                        validators=[
                            django.core.validators.RegexValidator(
                                message="Phone number must be in the format '0xxxxxxxxx' or '+66xxxxxxxxx'",
                                regex="^(\\+66|0)\\d{9}$",
                            )
                        ],
                    ),
                ),
                ("email", models.CharField(max_length=100)),
                ("password", models.CharField(max_length=255)),
                (
                    "password_again",
                    models.CharField(
                        max_length=255, verbose_name="Password confirmation"
                    ),
                ),
            ],
        ),
    ]
