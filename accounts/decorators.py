from django.http import HttpResponse
from django.shortcuts import redirect

# If the user is authenticated, send him to home
def unauthenticated_user(view_function):
    def wrapper_function(request, *args, **kwargs):

        if request.user.is_authenticated:
            return redirect('home')
        else:
            return view_function(request, *args, **kwargs)

    return wrapper_function

# if the user is in the restricted groups, redirect him to the 'unauthorized' page
def unallowed_users(unallowed_roles=[]):
    def decorator(view_function):
        def wrapper_function(request, *args, **kwargs):
            # Initialize the group
            group = None
            if request.user.groups.exists():
                # Re-assign the first group of the list
                group = request.user.groups.all()[0].name
            if group not in unallowed_roles:
                return view_function(request, *args, **kwargs)
            else:
                return redirect('unauthorized_page')
        return wrapper_function
    return decorator

# Redirect to user's page if Customers
def not_customer(view_function):
    def wrapper_function(request, *args, **kwargs):
        group = None
        if request.user.groups.exists():
            group = request.user.groups.all()[0].name
        if group == 'Customers':
            return redirect('user_page')
        else:
            return view_function(request, *args, **kwargs)
    return wrapper_function
