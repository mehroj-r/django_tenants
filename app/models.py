from django_tenants.models import TenantMixin, DomainMixin
from django.db import models


class Tenant(TenantMixin):
    name = models.CharField(max_length=255)

    created_app = models.DateField(auto_now_add=True)
    updated_app = models.DateField(auto_now=True)

class Domain(DomainMixin):
    pass

class TanentEmployee(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    address = models.ForeignKey('TanentAddress', on_delete=models.CASCADE)
    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE, null=True)

class TanentAddress(models.Model):
    old_id = models.BigIntegerField(null=True)
    street = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE, null=True)