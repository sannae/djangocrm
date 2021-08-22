from django.contrib import admin
# Import all models
from .models import *

# The admin panel! Where you *register* your models
admin.site.register(Tag)
admin.site.register(Customer)
admin.site.register(Product)
admin.site.register(Order)


