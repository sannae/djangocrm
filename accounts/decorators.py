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

# Check if logged user is within the allowed roles
def allowed_users(allowed_roles=[]):
    def decorator(view_function):
        def wrapper_function(request, *args, **kwargs):
            # Initialize the group
            group = None
            if request.user.groups.exists():
                # Re-assign the first group of the list
                group = request.user.groups.all()[0].name
            if group in allowed_roles:
                return view_function(request, *args, **kwargs)
            else:
                return HttpResponse('You are not authorized to view this page!')
        return wrapper_function
    return decorator

# Redirect to user's page if not admin
def admin_only(view_function):
    def wrapper_function(request, *args, **kwargs):
        group = None
        if request.user.groups.exists():
            group = request.user.groups.all()[0].name
        if group == 'Agents':
            return redirect('user_page')
        if group == 'Administrators':
            return view_function(request, *args, **kwargs)
    return wrapper_function
