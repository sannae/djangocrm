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
