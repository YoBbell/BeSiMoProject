from django.db import models
from django.core.validators import RegexValidator
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
import re
from django.contrib.auth.models import User

class Seller(models.Model):
    created_by = models.OneToOneField(User, related_name='seller', on_delete=models.CASCADE,)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    store_name = models.CharField(max_length=100, default='')
    password = models.CharField(max_length=100)
    
    phone_regex = RegexValidator(
        regex=r'^(\+66|0)\d{9}$',
        message="Phone number must be in the format '0xxxxxxxxx' or '+66xxxxxxxxx'")
    phone = models.CharField(validators=[phone_regex], max_length=12)
    
    email_regex = re.compile(r'^\d{9,11}@student\.chula\.ac\.th$')
    email = models.EmailField(unique=True)
    location = models.CharField(max_length=250, default='')
    store_image= models.ImageField(upload_to='uploads/seller_data/')
    qr_image= models.ImageField(upload_to='uploads/seller_data/')
    

    def clean(self):
        if not self.email_regex.match(self.email):
            raise ValidationError({'email': 'Email must be in the format: \'xxxxxxxxxx@student.chula.ac.th\''})

  
    def register(self):
        self.save()


    @staticmethod
    def get_seller_by_email(email):
        try:
            return Seller.objects.get(email= email)
        except:
            return False


    def isExists(self):
        if Seller.objects.filter(email = self.email):
            return True

        return False
    
    def update(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)
        self.save()
    
    def __str__(self):
        return self.name


class Category(models.Model):
    name= models.CharField(max_length=50)

    @staticmethod
    def get_all_categories():
        return Category.objects.all()

    def __str__(self):
        return self.name

    # ordering = models.IntegerField(default=0)

    # class Meta:
    #     ordering = ['ordering']
#-----------------------------------------------
class Item(models.Model):
    title = models.CharField(max_length=50)
    category = models.ForeignKey(Category, related_name='products', on_delete=models.CASCADE)
    seller = models.ForeignKey(Seller, related_name="products", on_delete=models.CASCADE)
    description = models.TextField(blank=True, null=True)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    added_date = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(upload_to='uploads/', blank=True, null=True)
    thumbnail = models.ImageField(upload_to='uploads/', blank=True, null=True) # Change uploads to thumbnails 

    class Meta:
        ordering = ['-added_date']

    def __str__(self):
        return self.title
