from .models import RegisterSeller, Product
from django import forms

class RegisterSellerForm(forms.ModelForm):
    class Meta:
        model = RegisterSeller
        fields = ['store_name','address','city','province','postal_code','business_type','business_description','primary_product_category','document']
        labels = {
            'store_name': 'Business/Store Name*',
            'address': 'Business Address*',
            'city': 'City*',
            'province': 'Province*',
            'postal_code': 'Postal Code*',
            'business_type':"Business Type*",
            'business_description': 'Business Description*',
            'primary_product_category': 'Primary Product Category*',
            'document': 'Upload Business Documents*'
        }

        widgets = {
            'store_name': forms.TextInput(attrs={'type': "text", 'id': "business-name"}),
            'address': forms.TextInput(attrs={'type': "text", 'id': "business-address"}),
            'city': forms.TextInput(attrs={'type': "text", 'id': "city"}),
            'province': forms.TextInput(attrs={'type': "text", 'id': "province"}),
            'postal_code': forms.TextInput(attrs={'type': "text", 'id': "postal-code"}),
            'business_description': forms.Textarea(attrs={'id': "business-description", 'rows': 4, 'style': 'resize: vertical;'}),
            'primary_product_category': forms.Select(attrs={'id': "primary-product-category"}),
            'document': forms.FileInput(attrs={'type':'file','id': "document"}),
            'registered_by': forms.TextInput(attrs={'type': "text", 'id': "registered-by"})
        }

    def save(self, commit=True, registered_by = None, **kwargs):
        seller = super().save(commit=False)
        seller.registered_by = registered_by  # Set registered_by from kwargs
        if commit:
            seller.save()
        return seller
    
class AddProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = '__all__'

        labels = {
            'name': 'Product Name *',
            'brand': 'Brand *',
            'price': 'Price (Rs.) *',
            'description': 'Product Description *',
            'image': 'Product Image *',
            'stock': 'Stock Quantity *',
            'category': 'Category *',
        }

        widgets = {
            'name': forms.TextInput(attrs={'type': "text", 'id': "product-name"}),
            'brand': forms.TextInput(attrs={'type': "text", 'id': "product-brand"}),
            'price': forms.NumberInput(attrs={'type': "number", 'id': "product-price", 'step': "0.01","min":"0"}),
            'description': forms.Textarea(attrs={'id': "product-description", 'rows': 4, 'style': 'resize: vertical;'}),
            'image': forms.FileInput(attrs={'type': "file", 'id': "product-image"}),
            'stock': forms.NumberInput(attrs={'type': "number", 'id': "product-stock",'min':'1'}),
            'category': forms.Select(attrs={'id': "product-category"}),
        }
        
