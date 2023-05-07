from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator
from django.db import models
from PIL import Image
from django.core.files import File
from io import BytesIO
import re
from django.db import models
from django.core.validators import RegexValidator
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
import re
import uuid


class Seller(models.Model):
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
    created_by = models.OneToOneField(User, related_name='vendor', on_delete=models.CASCADE, )


    def clean(self):
        if not self.email_regex.match(self.email):
            raise ValidationError({'email': 'Email must be in the format: \'xxxxxxxxxx@student.chula.ac.th\''})

        # if not validate_email(self.email):
        #     raise ValidationError({'email': 'Please enter a valid email address'})

    # email_regex = RegexValidator(
    #     regex=r'^\d{9,11}@student.chula.ac.th$',
    #     message="Email must be in the format: '6xxxxxxxxx@student.chula.ac.th'")
    # email = models.EmailField(validators=[email_regex], unique=True, error_messages={'invalid': 'Please enter a valid email address'})

    #to save the data
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

#-----------------------------------------------
# class Vendor(models.Model):
#     name = models.CharField(max_length=255)
#     created_at = models.DateTimeField(auto_now_add=True)
#     # created_by = models.OneToOneField(User, related_name='vendor', on_delete=models.CASCADE)

#     class Meta:
#         ordering = ['name']
    
#     def __str__(self):
#         return self.name

#     def get_balance(self):
#         items = self.items.filter(vendor_paid=False, order__vendors__in=[self.id])
#         return sum((item.product.price * item.quantity) for item in items)

#     def get_paid_amount(self):
#         items = self.items.filter(vendor_paid=True, order__vendors__in=[self.id])
#         return sum((item.product.price * item.quantity) for item in items)
#-----------------------------------------------
class Category(models.Model):
    name= models.CharField(max_length=50)
    # cat_image= models.ImageField(upload_to='uploads/categories/')

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
    Seller = models.ForeignKey(Seller, related_name="products", on_delete=models.CASCADE)
    description = models.TextField(blank=True, null=True)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    added_date = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(upload_to='uploads/', blank=True, null=True)
    thumbnail = models.ImageField(upload_to='uploads/', blank=True, null=True) # Change uploads to thumbnails 

    class Meta:
        ordering = ['-added_date']

    def __str__(self):
        return self.title

    
    def get_thumbnail(self):
        if self.thumbnail:
            return self.thumbnail.url
        else:
            if self.image:
                self.thumbnail = self.make_thumbnail(self.image)
                self.save()
                return self.thumbnail.url
            
            else:
                # Default Image
                return 'https://via.placeholder.com/240x180.jpg'
    
    # Generating Thumbnail - Thumbnail is created when get_thumbnail is called
    def make_thumbnail(self, image, size=(300, 200)):
        img = Image.open(image)
        img.convert('RGB')
        img.thumbnail(size)

        thumb_io = BytesIO()
        img.save(thumb_io, 'JPEG', quality=85)

        thumbnail = File(thumb_io, name=image.name)

        return thumbnail

#----------------------------------------------
class OrderItem(models.Model):
    item_id = models.UUIDField()
    quantity = models.IntegerField()
    payment_id = models.CharField(max_length=100)
    order_status = models.IntegerField() # 0: waiting to be shipped, 1: shipped, 2: arrived
    is_payout = models.BooleanField(default=False)
    tracking_number = models.CharField(max_length=100, null=True)
    shipping_company = models.CharField(max_length=100, null=True)
    website = models.CharField(max_length=255, null=True)

class ItemPicture(models.Model):
    item_id = models.UUIDField(default=uuid.uuid4)
    img_url = models.CharField(max_length=255)

    