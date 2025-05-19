from django.core.management.base import BaseCommand
from django_tenants.utils import get_tenant_model, schema_context

class Command(BaseCommand):
    help = "Fill the tenants field for each client schema"

    def handle(self, *args, **options):
        TenantModel = get_tenant_model()

        for tenant in TenantModel.objects.all():
            print(f"Switching to tenant schema: {tenant.schema_name}")

            with schema_context(tenant.schema_name):

                from client_app.models import Employee

                if tenant.schema_name == "public":
                    continue

                try:
                    employees = Employee.objects.filter(tenant=None)
                    employees.update(tenant=tenant)
                except Exception as e:
                    print(f"Error accessing schema {tenant.schema_name}: {e}")
