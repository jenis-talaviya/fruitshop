from rest_framework import serializers

from .models import Supply

class SupplySerializer(serializers.ModelSerializer):
    class Meta:
        model = Supply
        fields = "__all__"