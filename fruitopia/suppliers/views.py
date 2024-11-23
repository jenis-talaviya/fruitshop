from django.shortcuts import render
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Supplier
from .serializers import SuppliersSerializer
# Create your views here.

@api_view(["POST"])
def supplier_add(request):
        serializer = SuppliersSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET"])
def supplier_list(request):
    supplier = Supplier.objects.all()
    serializer = SuppliersSerializer(supplier, many=True)
    return Response(serializer.data)



@api_view(["PUT"])
def supplier_update(request):
    supplier_entered_pk = request.headers.get("pk1")
    if not supplier_entered_pk:
        return Response(
            {"error": "PK header is required"}, status=status.HTTP_400_BAD_REQUEST
        )

    try:
        supplier = Supplier.objects.get(pk=supplier_entered_pk)
    except Supplier.DoesNotExist:
        return Response(
            {"message": "supplier does not exist"}, status=status.HTTP_404_NOT_FOUND
        )
        
    serializer = SuppliersSerializer(supplier, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({"message": "Detail updated successfully", "data": serializer.data},status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



@api_view(["DELETE"])
def supplier_delete(request):
    supplier_entered_pk = request.headers.get("pk1")
    if not supplier_entered_pk:
        return Response(
            {"error": "PK header is required"}, status=status.HTTP_400_BAD_REQUEST
        )

    try:
        supplier = Supplier.objects.get(pk=supplier_entered_pk)
    except Supplier.DoesNotExist:
        return Response(
            {"message": "supplier does not exist"}, status=status.HTTP_404_NOT_FOUND
        )
    supplier.delete()
    return Response({"message": "supplier deleted successfully"})
