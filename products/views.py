from django.shortcuts import render
from .models import Product
from django.template.context_processors import csrf

# Create your views here.
def all_products(request):
    products = Product.objects.all()
    args = {}
    args.update(csrf(request))
    return render(request, "products.html", {"products": products}, args)