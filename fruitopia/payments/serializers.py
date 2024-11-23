from rest_framework import serializers

from .models import Payment

class PaymentsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = ['order', 'method', 'status', 'customer']