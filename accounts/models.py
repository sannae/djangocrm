from django.db import models

# Models file: building the database and classes objects here

class Customer(models.Model):
    name = models.CharField(max_length=200, null=True)     # String
    phone = models.CharField(max_length=200, null=True)     # String
    email = models.CharField(max_length=200, null=True)     # String
    date_created = models.DateTimeField(auto_now_add=True)  # Timestamp

    def __str__(self):
        return self.name

class Product(models.Model):

    # Values for category
    CATEGORY = (
        ('Indoor','Indoor'),
        ('Outdoor','Outdoor')
    )

    name = models.CharField(max_length=200, null=True)     # String
    price = models.FloatField(null=True)                    # Float
    category = models.CharField(max_length=200, null=True, choices=CATEGORY)     # String
    description = models.CharField(max_length=200, null=True)     # String
    date_created = models.DateTimeField(auto_now_add=True)  # Timestamp

    def __str__(self):
        return self.name

class Order(models.Model):

    # Values for status
    STATUS = (
        ('Pending','Pending'),
        ('Out for delivery','Out for delivery'),
        ('Delivered','Delivered')
    )

    # customer = 
    # product =
    date_created = models.DateTimeField(auto_now_add=True)  # Timestamp
    status = models.CharField(max_length=200, null=True, choices=STATUS)     # String with dropdown choices

    def __str__(self):
        return self.name