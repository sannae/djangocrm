from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.contrib.auth.models import User
from .models import Order

# Create order
class OrderForm(ModelForm):
    class Meta:
        model = Order
        fields = '__all__'     # Create a form with all the fields

# Create user
class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        # UserCreationForm documentation at https://docs.djangoproject.com/en/3.1/topics/forms/modelforms/#selecting-the-fields-to-use
        fields = [
            'username',
            'email',
            'password1',
            'password2'
        ]
