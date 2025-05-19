from django.urls import path
from django.contrib import admin

from app.views import index

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", index, name="index"),
]