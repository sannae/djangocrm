from django.shortcuts import render
from django.http import HttpResponse

# Our views, i.e. the rendered pages where the URLs will redirect

# Create your views here.

# Remember that you html templates needs to be stored in
# /APPNAME/templates/APPNAME/
# Because Django will automatically look for them there

def home(request):
    return render(request, 'accounts/dashboard.html')

def products(request):
    return render(request, 'accounts/products.html')

def customer(request):
    return render(request, 'accounts/customer.html')