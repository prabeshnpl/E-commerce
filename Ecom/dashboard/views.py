from django.shortcuts import render,redirect,get_object_or_404
from django.core.paginator import Paginator
from .models import CustomUser, Cart, Product,RegisterSeller, ProductImages
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login,logout,authenticate
from django.contrib import messages
import json
from .forms import RegisterSellerForm, AddProductForm
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
            phone = request.POST.get('phone')
            password = request.POST.get('password')
            confirm_password = request.POST.get('confirm-password')
            if password != confirm_password:
                messages.error(request,'Password didn\'t matched ! ')
                return render(request,'login.html')
            try:
                user = CustomUser.objects.create(first_name=full_name, email=email, phone_no=phone)
                user.set_password(password)
                user.save()
                if user:
                    messages.success(request,'Account Registration Successful ! ')

            except Exception as e:
                if 'UNIQUE constraint failed' in str(e):
                    messages.error(request,'Email and phone number must be unique.')
                else:
                    messages.error(request,str(e))

    return render(request,'login.html',{'page':'login'})

def Logout(request):
    logout(request)
    return redirect('home')

def home(request):
    return render(request, 'dashboard.html',{'page':'home'})

def products(request,pk):
    if not pk:
        return redirect('home')
    if not Product.objects.filter(id=pk).exists():
        messages.error(request,'Product not found ! ')
        return redirect('home')
    if request.method == 'POST':
        data = request.POST
        
    product = Product.objects.get(id=pk)  
    images = product.secondary_images.all()
    
    return render(request,'product.html',{'product':product,'images':images,'products':'home'})

def contact(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        message = request.POST.get('message')
        if not name or not email or not message:
            messages.error(request,'All fields are required ! ')
        else:
            messages.success(request,'Message sent successfully ! ')
            
    return render(request,'contact.html',{'page':'contact'})#page for active class in navbar

@login_required(redirect_field_name='login')
def registerseller(request):
    filled = False
    if RegisterSeller.objects.filter(registered_by = request.user).exists():
        filled = True
    if request.method == 'POST':
        if not filled:
            form = RegisterSellerForm(request.POST, request.FILES)
            if form.is_valid():
                seller = form.save(registered_by=request.user)
                messages.success(request,'Sucessfully Submitted ! Please wait for the teams\' review.')
            else:
                messages.error(request,form.errors)
        else:
            messages.error(request,'Form already filled. Please wait a while. ')

        return redirect('sellerdashboard')
    
    else:
        form = RegisterSellerForm()
            
    return render(request,'registerseller.html',{'form' : form ,'filled':filled,'page':'registerseller'})


@login_required(redirect_field_name='login')
def cart(request):
    try:
        cart_obj = get_object_or_404(Cart,user=request.user)
        products = cart_obj.products.all()
       
    except Exception as e:
        messages.error(request,str(e))
        
    return render(request, 'cart.html',{'products':products,'page':'cart'})

@login_required(redirect_field_name='login')
def sellerdashboard(request):
    if not request.user.is_seller:
        return redirect('cart')
    products = Product.objects.filter(seller=request.user)
    count = products.count()
    return render(request,'seller_dashboard.html',{'products':products,'count':count,'page':'sellerdashboard'})

@login_required(redirect_field_name='login')
def add_products(request):
    if not request.user.is_seller:
        return redirect('home')
    
    if request.method == 'POST':
        form = AddProductForm(request.POST,request.FILES)
        if form.is_valid():         
            form.save(seller = request.user)
            messages.success(request,'Product added successfully! ')
            return redirect('sellerdashboard')
        else:
            messages.error(request,form.errors)

    else:
        form = AddProductForm()
    return render(request,'add_products.html',{'form':form})


def load_products(request):
    page_no = request.GET.get('page',1) #if no pageno, default=1
    paginator = Paginator(Product.objects.all(),20)
    page = paginator.get_page(page_no)

    products = list(page.object_list.values('id','name','main_image','price','stock','brand'))
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
        

