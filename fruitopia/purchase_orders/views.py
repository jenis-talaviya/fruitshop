from django.shortcuts import render
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import PurchaseOrder
from .serializers import PurchaseOrderSerializer
# Create your views here.

@api_view(["POST"])
def purchaseorder_add(request):
        serializer = PurchaseOrderSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET"])
def purchaseorder_list(request):
    purchaseorder = PurchaseOrder.objects.all()
    serializer = PurchaseOrderSerializer(purchaseorder, many=True)
    return Response(serializer.data)



@api_view(["PUT"])
def purchaseorder_update(request):
    purchaseorder_entered_pk = request.headers.get("pk1")
    if not purchaseorder_entered_pk:
        return Response(
            {"error": "PK header is required"}, status=status.HTTP_400_BAD_REQUEST
        )

    try:
        purchaseorder = PurchaseOrder.objects.get(pk=purchaseorder_entered_pk)
    except PurchaseOrder.DoesNotExist:
        return Response(
            {"message": "order does not exist"}, status=status.HTTP_404_NOT_FOUND
        )
        
    serializer = PurchaseOrderSerializer(purchaseorder, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({"message": "Detail updated successfully", "data": serializer.data},status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



@api_view(["DELETE"])
def purchaseorder_delete(request):
    purchaseorder_entered_pk = request.headers.get("pk1")
    if not purchaseorder_entered_pk:
        return Response(
            {"error": "PK header is required"}, status=status.HTTP_400_BAD_REQUEST
        )

    try:
        purchaseorder = PurchaseOrder.objects.get(pk=purchaseorder_entered_pk)
    except PurchaseOrder.DoesNotExist:
        return Response(
            {"message": "purchase does not exist"}, status=status.HTTP_404_NOT_FOUND
        )
    purchaseorder.delete()
    return Response({"message": "purchase deleted successfully"})
