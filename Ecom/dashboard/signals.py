from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import CustomUser, Cart, RegisterSeller

@receiver(post_save,sender=CustomUser)
def create_Cart(sender,instance,created,**kwargs):
    if created:
        Cart.objects.create(user=instance)

@receiver(post_save,sender=RegisterSeller)
def update_user(sender,instance,created,**kwargs):
    if not created and instance.verified :
        user = instance.registered_by
        user.is_seller = True 
        user.save()
