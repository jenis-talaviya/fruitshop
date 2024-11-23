from django.shortcuts import render
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Supply
from .serializers import SupplySerializer
# Create your views here.

@api_view(["POST"])
def supply_add(request):
        serializer = SupplySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET"])
def supply_list(request):
    supply = Supply.objects.all()
    serializer = SupplySerializer(supply, many=True)
    return Response(serializer.data)



@api_view(["PUT"])
def supply_update(request):
    supply_entered_pk = request.headers.get("pk1")
    if not supply_entered_pk:
        return Response(
            {"error": "PK header is required"}, status=status.HTTP_400_BAD_REQUEST
        )

    try:
        supply = Supply.objects.get(pk=supply_entered_pk)
    except Supply.DoesNotExist:
        return Response(
            {"message": "supply does not exist"}, status=status.HTTP_404_NOT_FOUND
        )
        
    serializer = SupplySerializer(supply, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({"message": "Detail updated successfully", "data": serializer.data},status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



@api_view(["DELETE"])
def supply_delete(request):
    supply_entered_pk = request.headers.get("pk1")
    if not supply_entered_pk:
        return Response(
            {"error": "PK header is required"}, status=status.HTTP_400_BAD_REQUEST
        )

    try:
        supply = Supply.objects.get(pk=supply_entered_pk)
    except Supply.DoesNotExist:
        return Response(
            {"message": "supply does not exist"}, status=status.HTTP_404_NOT_FOUND
        )
    supply.delete()
    return Response({"message": "supply deleted successfully"})
