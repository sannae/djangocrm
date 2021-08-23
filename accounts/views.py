from django.shortcuts import render
from django.http import HttpResponse
from .models import *

# Our views, i.e. the rendered pages where the URLs will redirect

# To call your templates, you can use the django.shortcuts.render function.
# Remember that you html templates needs to be stored in
#   /APPNAME/templates/APPNAME/
# Because Django will automatically look for them there

def home(request):
    # Retrieving data from the database
    orders = Order.objects.all()
    customers = Customer.objects.all()
    # Totals for the status bar
    total_customers = customers.count()
    total_orders = orders.count()
    delivered_orders = orders.filter(status='Delivered').count()
    pending_orders = orders.filter(status='Pending').count()
    # Context to be passed to the template
    context = {
        'orders':orders,
        'customers':customers,
        'total_orders':total_orders,
        'delivered_orders':delivered_orders,
        'pending_orders':pending_orders
    }

    return render(request, 'accounts/dashboard.html', context)

def products(request):
    # Retrieving all the products from the database
    products = Product.objects.all()
    # The products dictionary will be passed to any function in the corresponding template
    return render(request, 'accounts/products.html', {'products':products})

def customer(request, pk_test):
    # Primary key
    customer = Customer.objects.get(id=pk_test)
    # Get all the selected customer's orders
    orders = customer.order_set.all()
    customer_total_orders = customer.order_set.count()
    # Context to be passed to the template
    context = {
        'customer':customer,
        'orders':orders,
        'customer_total_orders':customer_total_orders        
    }
    return render(request, 'accounts/customer.html', context)