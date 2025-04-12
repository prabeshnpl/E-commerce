from django.urls import path
from . import views

urlpatterns = [
    path('',views.home,name='home'), 
    
    path('cart/',views.cart,name='cart'), 
    path('seller_dashboard',views.sellerdashboard,name='sellerdashboard'),
    path('add_products/',views.add_products,name='add_products'),

    path('registerseller/',views.registerseller,name='registerseller'), 
    path('login/',views.Login,name='login'), 
    path('accounts/login/',views.Login,name='acc-login'), 
    path('logout/',views.Logout,name='logout'), 

    path('load_products/',views.load_products,name='load_products'),
    path('products/<int:pk>',views.products,name='products'),

    path('add_to_cart/',views.add_to_cart,name='add_to_cart'),
    path('remove_cart/',views.remove_cart,name='remove_cart'),
]