from django.shortcuts import render
from django.core.paginator import Paginator
from .models import CustomUser, Cart, CartProduct, Product
from django.http import JsonResponse
# Create your views here.
def home(request):
    return render(request, 'dashboard.html')

def load_products(request):
    page_no = request.GET.get('page',1) #if no pageno default=1
    paginator = Paginator(Product.objects.all(),20)
    page = paginator.get_page(page_no)

    products = list(page.object_list.values('id','name','image','price','description'))
    return JsonResponse({'products':products,'has_next':page.has_next()})


