from django.db import models
from django.contrib.auth.models import AbstractBaseUser,BaseUserManager,PermissionsMixin

# Create your models here.

class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(email, password, **extra_fields)

class CustomUser(AbstractBaseUser,PermissionsMixin):
    first_name = models.CharField(max_length=64)
    email = models.EmailField(unique=True)
    phone_no = models.IntegerField(unique=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_seller = models.BooleanField(default=False)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['phone_no']

    def __str__(self):
        return self.email

class Product(models.Model):
    class ProductType(models.TextChoices):
        CLOTHING = 'clothing', 'Clothing'
        ELECTRONICS = 'electronics', 'Electronics'
        ACCESSORIES = 'accessories', 'Accessories'
        FOOTWEAR = 'footwear', 'Footwear'
        WATCHES = 'watches', 'Watches'
        BAGS = 'bags', 'Bags'
        OTHER = 'other', 'Other'

    seller = models.ForeignKey(CustomUser, on_delete=models.CASCADE,related_name='products')
    name = models.CharField(max_length=64)
    brand = models.CharField(max_length=64)
    price = models.FloatField()
    main_image = models.ImageField(upload_to='product_images/')
    description = models.TextField()
    key_features = models.TextField()
    stock = models.IntegerField()
    category = models.CharField(max_length=64,choices=ProductType.choices,default=ProductType.OTHER)

    def __str__(self):
        return self.name

class ProductImages(models.Model):
    image = models.ImageField(upload_to='product_images/',null=True,blank=True)
    product = models.ForeignKey(Product,on_delete=models.CASCADE,related_name='secondary_images')

    def __str__(self):
        return f'{self.product.name}'


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

    registered_by = models.OneToOneField(CustomUser, related_name='seller', on_delete=models.CASCADE, unique=True)
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

