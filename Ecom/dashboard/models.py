from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

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


