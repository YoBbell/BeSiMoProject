from django.db import models
from django.core.validators import RegexValidator, EmailValidator


class Buyer(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)   
    telephone_number = models.CharField(
        max_length=17,
        validators=[
            RegexValidator(
                regex=r'^(\+66|0)[1-9]\d{8}$',
                message="Phone number must be entered in the format: '+66999999999' or '0999999999'."
            )
        ]
    )
    email = models.EmailField(validators=[EmailValidator()])


    def __str__(self):
        return f"{self.first_name} {self.last_name}"





