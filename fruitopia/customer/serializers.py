from rest_framework import serializers

from .models import Customers,Otp

class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customers
        fields = ["fname","lname","address","phone","email","password"]
        
class CustomerSerializerGet(serializers.ModelSerializer):
    class Meta:
        model = Customers
        fields = ["id","fname","lname","address","phone","email","password","created_at","updated_at","is_active","is_deleted","is_verify"]



#-------------------------------------------OTP-----------------------------------------------------
class OtpSerializer(serializers.ModelSerializer):
    class Meta:
        model = Otp
        fields = ["email","otp"]



class OtpSerializerOtpSent(serializers.ModelSerializer):
    class Meta:
        model = Otp
        fields = ["email"]