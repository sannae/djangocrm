from django.urls import path
from django.contrib.auth import views as auth_views
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
    path('unauthorized_page/', views.unauthorizedPage, name="unauthorized_page"),
    # User's settings
    path('user_settings/', views.userSettings, name="user_settings"),

    # Reset password: request form
    path('reset_password', auth_views.PasswordResetView.as_view(template_name="accounts/password_reset.html"), name="reset_password"),
    # Reset password: successfully sent the 'reset password link' message
    path('reset_password_sent', auth_views.PasswordResetDoneView.as_view(template_name="accounts/password_reset_sent.html"), name="password_reset_done"),
    # Reset password: Link gotten in email to reset the password: it requires the user's id encoded in base64, plus a token
    path('reset/<uidb64>/<token>', auth_views.PasswordResetConfirmView.as_view(template_name="accounts/password_reset_form.html"), name="password_reset_confirm"),
    # Reset password: process completed
    path('reset_password_complete', auth_views.PasswordResetCompleteView.as_view(template_name="accounts/password_reset_done.html"), name="password_reset_complete"),
]
