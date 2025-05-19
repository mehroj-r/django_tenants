from django.core.management.base import BaseCommand
from django_tenants.utils import get_tenant_model, schema_context

from app.models import TanentAddress, TanentEmployee

class Command(BaseCommand):
    help = "Fill the tenants field for each client schema"

    def handle(self, *args, **options):
        TenantModel = get_tenant_model()

        for tenant in TenantModel.objects.all():

            if tenant.schema_name in ["public"]:
                continue

            print(f"Switching to tenant schema: {tenant.schema_name}")


            with schema_context(tenant.schema_name):

                from client_app.models import Employee, Address

                try:
                    addresses = Address.objects.all()
                    for address in addresses:
                        TanentAddress.objects.create(
                            old_id=address.id,
                            street=address.street,
                            city=address.city,
                            country=address.country,
                            tenant=tenant,
                        )

                    employees = Employee.objects.all()
                    for employee in employees:
                        TanentEmployee.objects.create(
                            first_name=employee.first_name,
                            last_name=employee.last_name,
                            tenant=tenant,
                            address=TanentAddress.objects.get(old_id=employee.address.id, tenant=tenant),
                        )

                except Exception as e:
                    print(f"Error accessing schema {tenant.schema_name}: {e}")