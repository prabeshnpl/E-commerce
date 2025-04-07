from django.urls import path
from . import views

urlpatterns = [
    path('',views.home,name='home'), 
    path('login/',views.Login,name='login'), 
    path('logout/',views.Logout,name='logout'), 
    path('products/',views.load_products,name='products'),
    path('cart_products/',views.load_cart,name='cart_products'),
]