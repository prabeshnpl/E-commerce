from .models import RegisterSeller
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

        def save(self, commit=True, **kwargs):
            seller = super().save(commit=False)
            seller.registered_by = kwargs.get('registered_by')  # Set registered_by from kwargs
            if commit:
                seller.save()
            return seller