from django.db import models
from django.contrib.auth.models import User
from .constants import ACCOUNT_TYPE, GENDER_TYPE

# Create your models here.


class UserBankAccount(models.Model):
    user = models.OneToOneField(User, related_name='account', on_delete=models.CASCADE)  # related_name er maddhome user er attribiute jemon name ,gender,account_type ittadi access kora jay
    account_type = models.CharField(max_length=10, choices=ACCOUNT_TYPE)
    account_no = models.IntegerField(unique=True)               # unique mane duijoner account no kokhono same hbe na
    birth_date = models.DateField(null=True, blank=True)
    gender = models.CharField(max_length=10, choices=GENDER_TYPE)
    initial_deposite_date = models.DateField(auto_now=True)
    balance = models.DecimalField(default=0, max_digits=12, decimal_places=2)  # Decimal mane 12 digit nite parbe,,decimal_palace =2 mane doshomik er por duighor nibe
    
    def __str__(self):
         return str(self.account_no)
    


class UserAddress(models.Model):
    user = models.OneToOneField(User, related_name='address', on_delete=models.CASCADE)  # related_name er maddhome user er attribiute jemon name ,gender,account_type ittadi access kora jay
    street_address = models.CharField(max_length=150)
    city = models.CharField(max_length=100)
    postal_code = models.IntegerField()
    country = models.CharField(max_length=100)

    def __str__(self):
     return f"{self.user.email}"