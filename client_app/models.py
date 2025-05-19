from django.db import models

from app.models import Tenant


class Employee(models.Model):
    id = models.AutoField(primary_key=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    address = models.ForeignKey('Address', on_delete=models.CASCADE)
    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE, null=True)

class Address(models.Model):
    id = models.AutoField(primary_key=True)
    street = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return f'{self.street}, {self.city}, {self.country}'