from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.contrib.auth.models import Group
from .models import Customer

def customer_profile(sender, instance, created, **kwargs):
    if created:
        # Assign default group
        group = Group.objects.get(name='Customers')
        instance.groups.add(group)
        # Create a customer assigned to new user upon registration 
        Customer.objects.create(
            user=instance,
            name=instance.username,
            email=instance.email
        )
        print("Profile created!")

post_save.connect(customer_profile, sender=User)