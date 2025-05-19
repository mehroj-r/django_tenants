from django_tenants.models import TenantMixin, DomainMixin
from django.db import models


class Tenant(TenantMixin):
    name = models.CharField(max_length=255)

    created_app = models.DateField(auto_now_add=True)
    updated_app = models.DateField(auto_now=True)

class Domain(DomainMixin):
    pass