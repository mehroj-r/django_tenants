from django.core.management import BaseCommand
from django_tenants.utils import get_tenant_model, schema_context


class Command(BaseCommand):
    def handle(self, *args, **options):

        TenantModel = get_tenant_model()

        for tenant in TenantModel.objects.all():

            if tenant.schema_name in ["public"]:
                continue

            print(f"Switching to tenant schema: {tenant.schema_name}")

            with schema_context(tenant.schema_name):

                from client_app.models import Employee, EmployeeAddress

                try:
                    employees = Employee.objects.all()
                    for employee in employees:
                        EmployeeAddress.objects.create(employee=employee, address=employee.address)

                except Exception as e:
                    print(f"Error accessing schema {tenant.schema_name}: {e}")