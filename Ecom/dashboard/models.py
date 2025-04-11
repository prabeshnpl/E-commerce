from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)
    username = None
    phone_no = models.IntegerField(unique=True)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    is_seller = models.BooleanField(default=False)

    def __str__(self):
        return self.email

class Product(models.Model):
    name = models.CharField(max_length=64)
    brand = models.CharField(max_length=64,default='Django')
    price = models.FloatField()
    description = models.TextField()
    image = models.ImageField(upload_to='product_images/')

    stock = models.IntegerField()

    def __str__(self):
        return self.name

class Cart(models.Model):
    user = models.ForeignKey(CustomUser,on_delete=models.CASCADE,related_name='user_cart')
    products = models.ManyToManyField(Product,related_name='in_carts',blank=True)

    def __str__(self):
        return f"{self.user}'s cart"

class RegisterSeller(models.Model):
    class PrimaryProductCategory(models.TextChoices):
        CLOTHING = 'clothing', 'Clothing'
        ELECTRONICS = 'electronics', 'Electronics'
        HOME_APPLIANCES = 'home_appliances', 'Home Appliances'
        BOOKS = 'books', 'Books'
        OTHER = 'other', 'Other'
    
    class BusinessType(models.TextChoices):
        INDIVIDUAL = 'individual', 'Individual/Sole Proprietor'
        PARTNERSHIP = 'partnership', 'Partnership'
        LLC = 'llc', 'Limited Liability Company (LLC)'
        CORPORATION = 'corporation', 'Corporation'
        OTHER = 'other', 'Other'

    registered_by = models.ForeignKey(CustomUser, related_name='seller', on_delete=models.SET_NULL, null=True)
    store_name = models.CharField(max_length=64)
    address = models.CharField(max_length=64)
    city = models.CharField(max_length=64)
    province = models.CharField(max_length=64)
    postal_code = models.CharField(max_length=64)
    business_description = models.TextField()
    business_type = models.CharField(
        max_length=64,
        choices=BusinessType.choices,
        default=BusinessType.INDIVIDUAL,
    )
    primary_product_category = models.CharField(
        max_length=64,
        choices=PrimaryProductCategory.choices,
        default=PrimaryProductCategory.CLOTHING
    )
    document = models.FileField(upload_to='seller_documents/')
    
    verified = models.BooleanField(default=False)

    def __str__(self):
        return self.store_name

