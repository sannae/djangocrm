from django.urls import path
from . import views

# App URL manager

urlpatterns = [
    # Home page
    path('', views.home, name="home"),
    # Products page
    path('products/', views.products, name="products"),
    # Customer: pk (Primary key) comes from the customer view - this is a dynamic URL
    path('customer/<str:pk_test>', views.customer, name="customer")

]
