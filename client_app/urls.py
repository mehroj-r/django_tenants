from django.urls import path
from rest_framework import routers

from client_app.views import index, EmployeeViewset

urlpatterns = [
    path('', index, name='index'),
]

router = routers.DefaultRouter()
router.register('employee', EmployeeViewset)
urlpatterns += router.urls