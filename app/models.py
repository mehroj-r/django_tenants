from django.db import models


class Tenant(models.Model):
    name = models.CharField(max_length=255)

    created_app = models.DateField(auto_now_add=True)
    updated_app = models.DateField(auto_now=True)

class ClientEmployee(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE, null=True)