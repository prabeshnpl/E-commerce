from django.shortcuts import render,redirect,get_object_or_404
from django.core.paginator import Paginator
from .models import CustomUser, Cart, Product
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login,logout,authenticate
from django.contrib import messages
import json
# Create your views here.

def Login(request):
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        if request.POST.get('type') == 'login':
            email = request.POST.get('email')
            password = request.POST.get('password')
            user = authenticate(request,email=email,password=password)
            if user:
                login(request,user)
                return redirect('home')
            else:
                messages.error(request,'Invalid Credentials')
                return redirect('login')

        elif request.POST.get('type') == 'register':
            full_name = request.POST.get('fullname')
            email = request.POST.get('email')
            password = request.POST.get('password')
            confirm_password = request.POST.get('confirm-password')
            if password != confirm_password:
                messages.error(request,'Password didn\'t matched ! ')
                return render(request,'login.html')
            try:

                user = CustomUser.objects.create(first_name=full_name, email=email)
                user.set_password(password)
                user.save()
                if user:
                    messages.success(request,'Account Registration Successful ! ')

            except Exception as e:
                messages.error(request,str(e))

    return render(request,'login.html')

def Logout(request):
    logout(request)
    return redirect('home')

def home(request):
    return render(request, 'dashboard.html')

@login_required(redirect_field_name='login')
def cart(request):
    try:
        cart_obj = get_object_or_404(Cart,user=request.user)
        products = cart_obj.products.all()
    except Exception as e:
        messages.error(request,"User's cart not found !!")
        
    return render(request, 'cart.html',{'products':products})

def load_products(request):
    page_no = request.GET.get('page',1) #if no pageno, default=1
    paginator = Paginator(Product.objects.all(),20)
    page = paginator.get_page(page_no)

    products = list(page.object_list.values('id','name','image','price','description','stock'))
    return JsonResponse({'products':products,'has_next':page.has_next()})

@login_required(redirect_field_name='login')
def add_to_cart(request):
    if request.method == "POST":
        data = json.loads(request.body)
        id = data.get('id')
        product = Product.objects.get(id=id)    
        cart = Cart.objects.get(user=request.user)
        cart.products.add(product)
        cart.save()
        return JsonResponse({'message':data})
    return JsonResponse({'message':'error occured'})

@login_required(redirect_field_name='login')
def remove_cart(request):
    if request.method == "POST":
        data = json.loads(request.body)
        id = data.get('id')
        product = Product.objects.get(id=id)
        cart = Cart.objects.get(user=request.user)
        cart.products.remove(product)
        cart.save()
        return JsonResponse({"Message":'Removed successfully'})
        

