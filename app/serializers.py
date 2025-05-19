from rest_framework import serializers

from app.models import TenantEmployee, TenantAddress


class TenantEmployeeSerializer(serializers.ModelSerializer):

    class Meta:
        model = TenantEmployee
        fields = '__all__'


class TenantAddressSerializer(serializers.ModelSerializer):

    class Meta:
        model = TenantAddress
        fields = '__all__'