from accounts.decorators import *
from datetime import datetime
import calendar
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.forms import inlineformset_factory
from .models import *
from .forms import OrderForm, CreateUserForm, CustomerForm
from .filters import OrderFilter
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group
from django.contrib import messages
from collections import Counter

# Our views, i.e. the rendered pages where the URLs will redirect

# To call your templates, you can use the django.shortcuts.render function.
# Remember that you html templates needs to be stored in
#   /APPNAME/templates/APPNAME/
# Because Django will automatically look for them there

# Register
@unauthenticated_user # Only unauthenticated users
def registerPage(request):
    form = CreateUserForm()
    if request.method == "POST":
        form = CreateUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            email = form.cleaned_data.get('email')

            # Flash message: doc at https://docs.djangoproject.com/en/3.0/ref/contrib/messages/#using-messages-in-views-and-templates
            messages.success(request, 'Account was created for ' + username)
            return redirect('login') 
    context = {
        'form':form
    }
    return render(request, 'accounts/register.html', context)

# Log in
# Only unauthenticated users
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
# Only authenticated users
# Customers users are not authorized
@login_required(login_url='login')
@not_customer
def home(request):

    # Get user's regions 
    # (the list 'region' contains the user's related regions, depending on the assigned groups)
    userGroups = list(request.user.groups.all())
    groups = []
    for i in range(len(userGroups)):
        groups.append(userGroups[i].name)
    regions = []
    for i in range(len(userGroups)):
        regions.append(userGroups[i].id)

    # Retrieving data from the database
    if request.user.is_superuser:
        customers = Customer.objects.all().order_by('-date_created') 
        orders = Order.objects.all().order_by('-date_created') 
    else:
        customers = Customer.objects.all().filter(region_id__in=regions).order_by('-date_created') 
        orders = Order.objects.all().filter(customer_id__in=customers).order_by('-date_created') 
    
    # Totals for the status bar
    total_orders = orders.count()
    delivered_orders = orders.filter(status='Delivered').count()
    pending_orders = orders.filter(status='Pending').count()
    out_for_delivery_orders = orders.filter(status='Out for delivery').count()

    # Data for pie chart
    pie_chart_labels = ['Delivered', 'Pending', 'Out for delivery']
    pie_chart_data = [delivered_orders, pending_orders, out_for_delivery_orders]
    
    # Data for line chart
    this_month = datetime.today().month
    days_this_month = calendar.monthrange(9999,this_month)[1]
    list_days = list(range(1,days_this_month+1))
    orders_this_month = orders.filter(date_created__month = this_month)
    orders_cumulated = []
    delivered_cumulated = []
    out_for_delivery_cumulated = []
    pending_cumulated = []

    for day in list_days:

        # Day-by-day data
        orders_this_day = orders_this_month.filter(date_created__day = day)
        delivered_this_day = orders_this_month.filter(date_created__day = day, status='Delivered')
        out_for_delivery_this_day = orders_this_month.filter(date_created__day = day, status='Out for delivery')
        pending_this_day = orders_this_month.filter(date_created__day = day, status='Pending')

        # Count elements
        cumulated_orders_this_day = orders_this_day.count()
        cumulated_delivered = delivered_this_day.count()
        cumulated_out_for_delivery = out_for_delivery_this_day.count()
        cumulated_pending = pending_this_day.count()

        # Create list
        orders_cumulated.append(cumulated_orders_this_day)
        delivered_cumulated.append(cumulated_delivered)
        out_for_delivery_cumulated.append(cumulated_out_for_delivery)
        pending_cumulated.append(cumulated_pending)

    # Products sold in the current month
    products_this_month = []
    for i in range(len(orders_this_month)):
        products_this_month.append(orders_this_month[i].product.name)
    products_this_month_total = Counter(products_this_month)
    prod_this_months_names = list(dict(products_this_month_total).keys())
    prod_this_months_values = list(dict(products_this_month_total).values())

    # Context to be passed to the template
    context = {
        'orders':orders[0:5], # Last 5 orders
        'customers':customers[0:5], # Last 5 customers
        'total_orders':total_orders,
        'delivered_orders':delivered_orders,
        'pending_orders':pending_orders,
        'pie_chart_labels':pie_chart_labels,
        'pie_chart_data':pie_chart_data,
        'list_days':list_days,
        'orders_cumulated':orders_cumulated,
        'delivered_cumulated':delivered_cumulated,
        'out_for_delivery_cumulated':out_for_delivery_cumulated,
        'pending_cumulated':pending_cumulated,
        'prod_this_month_names':prod_this_months_names,
        'prod_this_month_values':prod_this_months_values
    }

    return render(request, 'accounts/dashboard.html', context)

# Products page
# Only authenticated users
# Customers not allowed
@login_required(login_url='login')
@unallowed_users(unallowed_roles=['Customers'])
def products(request):
    # Retrieving all the products from the database
    products = Product.objects.all()
    # The products dictionary will be passed to any function in the corresponding template
    return render(request, 'accounts/products.html', {'products':products})

# Customer view
# Only authenticated users
@login_required(login_url='login')
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
# Only authenticated users
# No Customers allowed
@login_required(login_url='login')
@unallowed_users(unallowed_roles=['Customers'])
def createOrder(request, pk):

    # Form set (use either 'form' or 'formset' properties)
    OrderFormSet = inlineformset_factory(Customer, Order, fields=('product','status','notes'), extra=5)
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
# Only authenticated users
# No Customers allowed
@login_required(login_url='login')
@unallowed_users(unallowed_roles=['Customers'])
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
# Only authenticated users
# No Customers allowed
@login_required(login_url='login')
@unallowed_users(unallowed_roles=['Customers'])
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
# Only authenticated users
@login_required(login_url='login')
def userPage(request):

    # user's Groups and Regions IDs
    userGroups = list(request.user.groups.all())
    groups = []
    for i in range(len(userGroups)):
        groups.append(userGroups[i].name)
    regions = []
    for i in range(len(userGroups)):
        regions.append(userGroups[i].id)

    # if user is Admin, see everything
    if request.user.is_superuser:
        orders = Order.objects.all().order_by('-date_created')
    # if user is Customer, see only his orders
    elif 'Customers' in groups:
        orders = request.user.customer.order_set.all().order_by('-date_created') 
    # if user is Agent, see only orders from assigned regions
    else:
        customers = Customer.objects.all().filter(region_id__in=regions)
        orders = Order.objects.all().filter(customer_id__in=customers).order_by('-date_created')        

    # Status bar
    total_orders = orders.count()
    delivered_orders = orders.filter(status='Delivered').count()
    pending_orders = orders.filter(status='Pending').count()

    context = {
       'orders':orders,
       'total_orders':total_orders,
       'delivered_orders':delivered_orders,
       'pending_orders':pending_orders
    }
    return render(request, 'accounts/user.html', context)

# Unauthorized error page
def unauthorizedPage(request):
    # Context to be passed to the template
    context = {
        
    }
    return render(request, 'accounts/unauthorized.html', context)

# User's settings page
@login_required(login_url='login')
def userSettings(request):
    # logged-in user
    customer = request.user.customer
    # Render the form
    form = CustomerForm(instance=customer)
    # Submit (including files!)
    if request.method == 'POST':
        form = CustomerForm(request.POST, request.FILES, instance=customer)
        if form.is_valid():
            form.save()
    # Context to be passed to the template
    context = {
        'form': form
    }
    return render(request, 'accounts/user_settings.html', context)