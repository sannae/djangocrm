from accounts.decorators import *
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.forms import inlineformset_factory
from .models import *
from .forms import OrderForm, CreateUserForm
from .filters import OrderFilter
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group
from django.contrib import messages

# Our views, i.e. the rendered pages where the URLs will redirect

# To call your templates, you can use the django.shortcuts.render function.
# Remember that you html templates needs to be stored in
#   /APPNAME/templates/APPNAME/
# Because Django will automatically look for them there

# Register
@unauthenticated_user
def registerPage(request):
    form = CreateUserForm()
    if request.method == "POST":
        form = CreateUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            # Assign default group
            group = Group.objects.get(name='Customers')
            user.groups.add(group)
            # Create a customer assigned to new user upon registration 
            # Customer.objects.create(
            #     user=user,
            # )
            # Flash message: doc at https://docs.djangoproject.com/en/3.0/ref/contrib/messages/#using-messages-in-views-and-templates
            messages.success(request, 'Account was created for ' + username)
            return redirect('login') 
    context = {
        'form':form
    }
    return render(request, 'accounts/register.html', context)

# Log in
@unauthenticated_user
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
        else:
            messages.info(request, "Username OR password is incorrect!")

    context = {}
    return render(request, 'accounts/login.html', context)

# Logout user
def logoutUser(request):
    # Logout the user
    logout(request)
    return redirect('login')

# Dashboard
@login_required(login_url='login')
@admin_only
def home(request):

    # Get user's regions 
    # (the list 'region' contains the user's related regions, depending on the assigned groups)
    userGroups = list(request.user.groups.all())
    regions = []
    for i in range(len(userGroups)):
        regions.append(userGroups[i].name)

    # Retrieving data from the database
    orders = Order.objects.all()
    customers = Customer.objects.all()
    

    #if request.user.groups not in ['Administrators']:
    #   filtered_customers = customers.filter(Region.name in regions)
    #   print(filtered_customers)
    
    # Totals for the status bar
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
@login_required(login_url='login')
@allowed_users(allowed_roles=['Administrators'])
def products(request):
    # Retrieving all the products from the database
    products = Product.objects.all()
    # The products dictionary will be passed to any function in the corresponding template
    return render(request, 'accounts/products.html', {'products':products})

# Customer view
@login_required(login_url='login')
@allowed_users(allowed_roles=['Administrators'])
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
@login_required(login_url='login')
@allowed_users(allowed_roles=['Administrators'])
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
@login_required(login_url='login')
@allowed_users(allowed_roles=['Administrators'])
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
@login_required(login_url='login')
@allowed_users(allowed_roles=['Administrators'])
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

# User's page
@login_required(login_url='login')
def userPage(request):

    username = request.user.username
    
    
    # Customer's orders
    #orders = request.user.customer.order_set.all()

    # Status bar
    # total_orders = orders.count()
    # delivered_orders = orders.filter(status='Delivered').count()
    # pending_orders = orders.filter(status='Pending').count()

    context = {



       # 'orders':orders,
       # 'total_orders':total_orders,
       # 'delivered_orders':delivered_orders,
       # 'pending_orders':pending_orders
    }
    return render(request, 'accounts/user.html', context)