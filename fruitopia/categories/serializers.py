from rest_framework import serializers

from .models import Categories

class CategoriesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Categories
        fields = "__all__"
        
# class CustomerSerializerGet(serializers.ModelSerializer):
#     class Meta:
#         model = Customers
#         fields = ["id","fname","lname","address","phone","email","password","created_at","updated_at","is_active","is_deleted","is_verify"]
