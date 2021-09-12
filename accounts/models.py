from django.db import models
from django.contrib.auth.models import User

# Models file: building the database and classes objects here

class Customer(models.Model):
    user = models.OneToOneField(User, null=True, on_delete=models.CASCADE)  # One-to-one with user
    name = models.CharField(max_length=200, null=True)     # String
    phone = models.CharField(max_length=200, null=True, blank=True)     # String
    address = models.CharField(max_length=200, null=True, blank=True)   # String
    email = models.CharField(max_length=200, null=True)     # String
    date_created = models.DateTimeField(auto_now_add=True)  # Timestamp

    def __str__(self):
        return self.name

class Tag(models.Model):
    name = models.CharField(max_length=200, null=True)     # String

    def __str__(self):
        return self.name

class Product(models.Model):

    # Values for category
    CATEGORY = (
        ('Hardware','Hardware'),
        ('Software','Software'),
    )

    name = models.CharField(max_length=200, null=True)     # String
    price = models.FloatField(null=True)                    # Float
    category = models.CharField(max_length=200, null=True, choices=CATEGORY)     # String
    description = models.CharField(max_length=200, null=True, blank=True)     # String, can be blank
    date_created = models.DateTimeField(auto_now_add=True)  # Timestamp
    # Many to many relationship with Tag (a product can have many tags associated, the same tag can be associated to many products)
    tag = models.ManyToManyField(Tag)
 
    def __str__(self):
        return self.name

class Order(models.Model):

    # Values for status
    STATUS = (
        ('Pending','Pending'),
        ('Out for delivery','Out for delivery'),
        ('Delivered','Delivered')
    )

    # Foreign key on the Customers table: set null if customer is deleted
    customer = models.ForeignKey(Customer, null=True, on_delete = models.SET_NULL) 
    # Foreign key on the Product table: set null if product is deleted
    product = models.ForeignKey(Product, null=True, on_delete=models.SET_NULL)
    # Other fields
    date_created = models.DateTimeField(auto_now_add=True)  # Timestamp
    status = models.CharField(max_length=200, null=True, choices=STATUS)     # String with dropdown choices
    notes = models.CharField(max_length=200, null=True, blank=True)

    # Return the corresponding product's name
    def __str__(self):
        return self.product.name