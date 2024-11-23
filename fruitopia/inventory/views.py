from django.shortcuts import render

from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Inventory
from .serializers import InventorySerializer

# Create your views here.

@api_view(["POST"])
def inventory_add(request):
        serializer = InventorySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET"])
def inventory_list(request):
    inventory = Inventory.objects.all()
    serializer = InventorySerializer(inventory, many=True)
    return Response(serializer.data)



@api_view(["PUT"])
def inventory_update(request):
    inventory_entered_pk = request.headers.get("pk1")
    if not inventory_entered_pk:
        return Response(
            {"error": "PK header is required"}, status=status.HTTP_400_BAD_REQUEST
        )

    try:
        inventory = Inventory.objects.get(pk=inventory_entered_pk)
    except Inventory.DoesNotExist:
        return Response(
            {"message": "inventory does not exist"}, status=status.HTTP_404_NOT_FOUND
        )
        
    serializer = InventorySerializer(inventory, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({"message": "Detail updated successfully", "data": serializer.data},status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



@api_view(["DELETE"])
def inventory_delete(request):
    inventory_entered_pk = request.headers.get("pk1")
    if not inventory_entered_pk:
        return Response(
            {"error": "PK header is required"}, status=status.HTTP_400_BAD_REQUEST
        )

    try:
        inventory = Inventory.objects.get(pk=inventory_entered_pk)
    except Inventory.DoesNotExist:
        return Response(
            {"message": "inventory does not exist"}, status=status.HTTP_404_NOT_FOUND
        )
    inventory.delete()
    return Response({"message": "inventory deleted successfully"})
