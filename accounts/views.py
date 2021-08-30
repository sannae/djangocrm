from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.forms import inlineformset_factory
from .models import *
from .forms import OrderForm, CreateUserForm
from .filters import OrderFilter
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages

# Our views, i.e. the rendered pages where the URLs will redirect

# To call your templates, you can use the django.shortcuts.render function.
# Remember that you html templates needs to be stored in
#   /APPNAME/templates/APPNAME/
# Because Django will automatically look for them there

# Register
def registerPage(request):
    form = CreateUserForm()
    if request.method == "POST":
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            user = form.cleaned_data.get('username')
            # Flash message: doc at https://docs.djangoproject.com/en/3.0/ref/contrib/messages/#using-messages-in-views-and-templates
            messages.success(request, 'Account was created for ' + user)
            return redirect('login') 
    context = {
        'form':form
    }
    return render(request, 'accounts/register.html', context)

# Log in
def loginPage(request):
    if request.method == "POST":
        # Get username and password from POST request
        username = request.POST.get('username')
        password = request.POST.get('password')
        # Authenticate
        user = authenticate(request, username=username, password=password)
        # Login user
        if user is not None:
            login(request, user)
            return redirect('home')
    context = {}
    return render(request, 'accounts/login.html', context)

# Dashboard
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

# Products page
def products(request):
    # Retrieving all the products from the database
    products = Product.objects.all()
    # The products dictionary will be passed to any function in the corresponding template
    return render(request, 'accounts/products.html', {'products':products})

# Customer view
def customer(request, pk_test):
    # Primary key
    customer = Customer.objects.get(id=pk_test)
    # Get all the selected customer's orders
    orders = customer.order_set.all()
    customer_total_orders = customer.order_set.count()
    # reset the orders variable wit the filter, depending on the GET request
    myFilter = OrderFilter(request.GET, queryset=orders)
    orders = myFilter.qs
    # Context to be passed to the template
    context = {
        'customer':customer,
        'orders':orders,
        'customer_total_orders':customer_total_orders,
        'myFilter':myFilter     
    }
    return render(request, 'accounts/customer.html', context)

# Create order form
def createOrder(request, pk):

    # Form set (use either 'form' or 'formset' properties)
    OrderFormSet = inlineformset_factory(Customer, Order, fields=('product','status'), extra=5)
    customer = Customer.objects.get(id=pk)
    # No initial objects in the formset
    formSet = OrderFormSet(queryset = Order.objects.none(), instance=customer)

    # Form from forms.py
    # Initial instance of the customer is the belongin customer itself
    # form = OrderForm(initial={'customer':customer})
    if request.method == "POST":
        # print('Printing POST:', request.POST) ## Testing
        # form = OrderForm(request.POST)
        formSet = OrderFormSet(request.POST, instance=customer)
        # Save a new instance in the database when submitting
        if formSet.is_valid():
            formSet.save()
            # Redirect to dashboard
            return redirect('/')

    # Context to be passed to the template
    context = {
        'formSet':formSet      
    }
    return render(request, 'accounts/order_form.html', context)

# Update order form
def updateOrder(request, pk):

    # Get the order with the corresponding primary key 
    order = Order.objects.get(id=pk)
    # Pre-fill the form with the selected order
    form = OrderForm(instance=order)
    # Save the same instance when submitting
    if request.method == "POST":
        form = OrderForm(request.POST, instance=order)
        # Save the form data in the database
        if form.is_valid():
            form.save()
            # Redirect to dashboard
            return redirect('/')
    # Context to be passed to the template
    context = {
        'form':form        
    }
    return render(request, 'accounts/order_form.html', context)

# Delete order form
def deleteOrder(request, pk):

    # Order to be deleted
    order = Order.objects.get(id=pk)

    # Actual deletion
    if request.method == "POST":
        order.delete()
        # Go back to home
        return redirect('/')

    context = {
        'order':order 
    }

    return render(request, 'accounts/delete.html', context)