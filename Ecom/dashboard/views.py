from django.shortcuts import render,redirect
from django.core.paginator import Paginator
from .models import CustomUser, Cart, CartProduct, Product
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login,logout,authenticate
from django.contrib import messages
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
    print(request.user)
    return render(request, 'dashboard.html')

# @login_required(login_url='login/')
def load_products(request):
    page_no = request.GET.get('page',1) #if no pageno, default=1
    paginator = Paginator(Product.objects.all(),20)
    page = paginator.get_page(page_no)

    products = list(page.object_list.values('id','name','image','price','description','stock'))
    return JsonResponse({'products':products,'has_next':page.has_next()})

@login_required(login_url='login/')
def load_cart(request):
    cart_obj = Cart.objects.get(user=request.user)
    cart_products = cart_obj.products.all()
    return JsonResponse({'cart_products': list(cart_products.values('id','name','image','price','description','stock'))})




