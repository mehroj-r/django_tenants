from django.http import HttpResponse
from rest_framework import viewsets

from app.models import TenantEmployee, TenantAddress
from client_app.serializers import EmployeeSerializer, AddressSerializer


def index(request):
    return HttpResponse("<h1> PUBLIC TENANT <h1/>")

class EmployeeViewset(viewsets.ModelViewSet):
    queryset = TenantEmployee.objects.all()
    serializer_class = EmployeeSerializer

class AddressViewset(viewsets.ModelViewSet):
    queryset = TenantAddress.objects.all()
    serializer_class = AddressSerializer
