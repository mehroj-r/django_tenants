from django.urls import path
from django.contrib import admin
from rest_framework import routers

from app.views import index, AddressViewset, EmployeeViewset

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", index, name="index"),
]

router = routers.DefaultRouter()

router.register("employee", EmployeeViewset, basename="employee")
router.register("address", AddressViewset, basename="address")

urlpatterns += router.urls