from rest_framework import serializers

from .models import OrderItem

class OrdersItemsSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = "__all__"