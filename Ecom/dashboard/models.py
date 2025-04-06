from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class CustomUser(AbstractUser):
    pass

class Product(models.Model):
    name = models.CharField(max_length=64)
    price = models.FloatField()
    description = models.TextField()
    image = models.ImageField(upload_to='product_images/')
    stock = models.IntegerField()

class Cart(models.Model):
    user = models.ForeignKey(CustomUser,on_delete=models.CASCADE,related_name='user_cart')
    products = models.ManyToManyField(Product,related_name='in_carts',through="CartProduct",blank=True)

class CartProduct(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    no_of_product = models.IntegerField()

    class Meta:
        unique_together = ('product','cart')
