from django.urls import path
from . import views

urlpatterns = [
    path('',views.home,name='home'), 
    path('cart/',views.cart,name='cart'), 
    path('login/',views.Login,name='login'), 
    path('accounts/login/',views.Login,name='acc-login'), 
    path('logout/',views.Logout,name='logout'), 
    path('products/',views.load_products,name='products'),
    path('add_to_cart/',views.add_to_cart,name='add_to_cart'),
    path('remove_cart/',views.remove_cart,name='remove_cart'),
]