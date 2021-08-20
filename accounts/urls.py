from django.urls import path
from . import views

# App URL manager

urlpatterns = [
    path('', views.home),    # Home
    path('products/', views.products),   # Products
    path('customer/', views.customer),    # Customer
]
