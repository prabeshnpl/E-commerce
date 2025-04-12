from .models import RegisterSeller, Product, ProductImages
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
    image1 = forms.ImageField(required=False, widget=forms.FileInput(attrs={'type': "file", 'id': "productImage1", 'accept': "image/*"}))
    image2 = forms.ImageField(required=False, widget=forms.FileInput(attrs={'type': "file", 'id': "productImage2", 'accept': "image/*"}))
    class Meta:
        model = Product
        exclude = ['seller']

        labels = {
            'name': 'Product Name *',
            'brand': 'Brand *',
            'price': 'Price (Rs.) *',
            'description': 'Product Description *',
            'main_image': 'Product Image *',
            'stock': 'Stock Quantity *',
            'category': 'Category *',
            'key_features':'Key Features',
        }

        widgets = {
            'name': forms.TextInput(attrs={'type': "text", 'id': "product-name"}),
            'brand': forms.TextInput(attrs={'type': "text", 'id': "product-brand"}),
            'price': forms.NumberInput(attrs={'type': "number", 'id': "product-price", 'step': "0.01","min":"0"}),
            'description': forms.Textarea(attrs={'id': "product-description", 'rows': 4, 'style': 'resize: vertical;'}),
            'key_features': forms.Textarea(attrs={'id': "product-features", 'placeholder':'Enter each feature on a new line', 'rows': 4, 'style': 'resize: vertical;'}),
            'main_image': forms.FileInput(attrs={'type': "file", 'id': "mainProductImage",'accept':"image/*"}),
            'stock': forms.NumberInput(attrs={'type': "number", 'id': "product-stock",'min':'1'}),
            'category': forms.Select(attrs={'id': "product-category"}),
        }

    def save(self, commit = True, seller=None, **kwargs):
        product = super().save(commit=False)
        product.seller = seller
        if commit:
            product.save()
            image1 = self.cleaned_data.get('image1')
            image2 = self.cleaned_data.get('image2')

            if image1:
                ProductImages.objects.create(product=product, image=image1)
            if image2:
                ProductImages.objects.create(product=product, image=image2)
        
        return product


        
