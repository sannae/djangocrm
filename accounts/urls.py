from django.urls import path
from . import views

# App URL manager

urlpatterns = [
    # Register
    path('register/', views.registerPage, name="register"),
    # Log in
    path('login/', views.loginPage, name="login"),
    # Log out
    path('logout/', views.logoutUser, name="logout"),
    # Home page
    path('', views.home, name="home"),
    # Products page
    path('products/', views.products, name="products"),
    # Customer: pk (Primary key) comes from the customer view - this is a dynamic URL
    path('customer/<str:pk_test>', views.customer, name="customer"),
    # Create order form
    path('order_form/<str:pk>', views.createOrder, name="create_order"),
    # Update order form
    path('update_order/<str:pk>', views.updateOrder, name="update_order"),
    # Delete order form
    path('delete_order/<str:pk>', views.deleteOrder, name="delete_order"),
    # User's profile
    path('user/', views.userPage, name="user_page"),
    # Unauthorized error page
    path('unauthorized_page/', views.unauthorizedPage, name="unauthorized_page")
]
