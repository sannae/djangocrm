# Generated by Django 3.2.6 on 2021-09-25 22:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0016_customer_profile_pic'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customer',
            name='profile_pic',
            field=models.ImageField(blank=True, default='blank_profile.png', null=True, upload_to=''),
        ),
    ]