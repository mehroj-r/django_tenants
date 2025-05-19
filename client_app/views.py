from django.http import HttpResponse
from rest_framework import viewsets

from client_app.models import Employee, Address
from client_app.serializers import EmployeeSerializer, AddressSerializer


def index(request):
    return HttpResponse(f"<h1> {request.tenant} Index </h1>")

class EmployeeViewset(viewsets.ModelViewSet):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer

class AddressViewset(viewsets.ModelViewSet):
    queryset = Address.objects.all()
    serializer_class = AddressSerializer
