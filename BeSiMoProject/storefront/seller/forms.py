from django import forms
from .models import Seller

class SellerForm(forms.ModelForm):
    class Meta:
        model = Seller
        fields = ['store_name', 'seller_name', 'seller_phone', 'store_address', 'store_image', 'qr_code','username_email','password']
        labels = {
            'store_name': 'Store Name',
            'seller_name': 'Seller Name',
            'seller_phone': 'Seller Phone',
            'store_address': 'Store Address',
            'username_email' : 'Username',
            'password' : 'Password',
            'store_image': 'Picture of Store',
            'qr_code': 'QR Code Picture',
           
        }
