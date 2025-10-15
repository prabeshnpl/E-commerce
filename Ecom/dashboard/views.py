from django.shortcuts import render,redirect,get_object_or_404
from django.core.paginator import Paginator
from .models import CustomUser, Cart, Product,RegisterSeller, Order, MiniOrder
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login,logout,authenticate
from django.contrib import messages
from .forms import RegisterSellerForm, AddProductForm
from datetime import datetime, timedelta
import requests, uuid, hmac, hashlib, base64, json

# Create your views here.

def generate_esewa_signature(msg, secret_key):
    try:
        hmac_sha256 = hmac.new(secret_key.encode("utf-8"), msg.encode("utf-8"), hashlib.sha256)
        digest = hmac_sha256.digest()
        signature = base64.b64encode(digest).decode('utf-8') 
        
        return signature
    except Exception as e:
        print(repr(e))
        raise ValueError(e)

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
    try:
        product = get_object_or_404(Product,id=pk)
        if not pk:
            return redirect('home')
        if request.method == 'POST':
            data = request.POST
            quantity = data['quantity']
            amount = product.price * int(quantity)
            tax_amount = amount * 0.13
            total_price = amount +tax_amount
            shipping_address = data['address']
            shipping_city = data['city']
            shipping_province = data['province']
            payment_method = data['payment_method']
            tracking_number = str(uuid.uuid4()).replace('-', '').upper()[:12]
            delivery_date = datetime.now() + timedelta(weeks=1)

            order = Order.objects.create(
                buyer=request.user,
                total_amount=total_price + int(135),
                shipping_address=shipping_address,
                shipping_city=shipping_city,
                shipping_province=shipping_province,
                payment_method=payment_method,
                tracking_number=tracking_number,
                delivery_date=delivery_date,
            )
            MiniOrder.objects.create(
                product=product,
                order=order,
                quantity=quantity,
                price=total_price / int(quantity),
                seller=product.seller,
                tracking_number=tracking_number
            )

            if payment_method == "esewa" or payment_method == "card":
                payload = esewa_payment(
                    total_amount=total_price,
                    amount=amount,
                    tax_amount=tax_amount,
                    product_code="EPAYTEST",
                    product_delivery_charge=0,
                    product_service_charge=0,
                    transaction_uuid=tracking_number
                )
                return render(request, "esewa_payment.html", {
                    "payload": payload
                })
            
            messages.success(request, f'Order placed successfully! Tracking Number: {tracking_number}')
            return redirect('cart')
    except Exception as e:
        messages.error(request,str(e))
        return redirect('home')
      
    images = product.secondary_images.all()
    
    return render(request,'product.html',{'product':product,'images':images,'page':'home'})

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
        
    return render(request, 'cart.html',{'products':products,'page':'cart','orders':Order.objects.filter(buyer=request.user).order_by('-order_date')})

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
        
def esewa_payment(total_amount, amount, tax_amount, product_code, product_service_charge, product_delivery_charge, transaction_uuid):

    secret_key = "8gBm/:&EnhH.1/q"
    signed_field_names = "amount,tax_amount,total_amount,transaction_uuid,product_code"
    msg = f"amount={amount},tax_amount={tax_amount},total_amount={total_amount},transaction_uuid={transaction_uuid},product_code={product_code}"

    signature = generate_esewa_signature(msg=msg, secret_key=secret_key)
    
    payload = {
    "amount": amount,
    "failure_url": "http://127.0.0.1:8000/esewa-failure/",
    "product_delivery_charge": product_delivery_charge,
    "product_service_charge": product_service_charge,
    "product_code": product_code,
    "signature": signature,
    "signed_field_names": signed_field_names,
    "success_url": "http://127.0.0.1:8000/esewa-success/",
    "tax_amount": tax_amount,
    "total_amount": total_amount,
    "transaction_uuid": transaction_uuid
    }
    return payload

# @csrf_exempt
def esewa_success(request):
    encoded_data = request.GET.get("data")

    decoded_bytes = base64.b64decode(encoded_data)
    decoded_str = decoded_bytes.decode("utf-8")

    payload = json.loads(decoded_str)
    print(payload)

    status = payload.get("status")
    tracking_number = payload.get("transaction_uuid")
    order = Order.objects.get(tracking_number=tracking_number)

    if status == "COMPLETE":        
        order.payment_method = "completed"
        order.save()
        return render(request, "esewa_after_payment.html", {"success":True, "failure":False})

    miniorder = MiniOrder.objects.get(order__id=order.id)
    miniorder.delete()
    order.delete()
    return render("esewa_after_payment.html", {"success":False, "failure":True})
    

# @csrf_exempt
def esewa_failure(request):
    print("Failed")
    return render(request, "esewa_after_payment.html", {"success":False, "failure":True})

def verify_esewa_transaction(pid, amt, ref_id):
    url = "https://uat.esewa.com.np/epay/transrec"
    payload = {
        'amt': amt,
        'scd': 'EPAYTEST',  # Replace with your merchant code
        'pid': pid,
        'rid': ref_id
    }
    response = requests.post(url, data=payload)
    return "Success" in response.text
