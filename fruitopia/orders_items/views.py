from django.shortcuts import render
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import OrderItem
from .serializers import OrdersItemsSerializer
# Create your views here.

@api_view(["POST"])
def orderitems_add(request):
        serializer = OrdersItemsSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET"])
def orderitems_list(request):
    orderitems = OrderItem.objects.all()
    serializer = OrdersItemsSerializer(orderitems, many=True)
    return Response(serializer.data)



@api_view(["PUT"])
def orderitems_update(request):
    orderitems_entered_pk = request.headers.get("pk1")
    if not orderitems_entered_pk:
        return Response(
            {"error": "PK header is required"}, status=status.HTTP_400_BAD_REQUEST
        )

    try:
        order = OrderItem.objects.get(pk=orderitems_entered_pk)
    except OrderItem.DoesNotExist:
        return Response(
            {"message": "order items does not exist"}, status=status.HTTP_404_NOT_FOUND
        )

    serializer = OrdersItemsSerializer(order, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({"message": "Detail updated successfully", "data": serializer.data},status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



@api_view(["DELETE"])
def orderitems_delete(request):
    orderitems_entered_pk = request.headers.get("pk1")
    if not orderitems_entered_pk:
        return Response(
            {"error": "PK header is required"}, status=status.HTTP_400_BAD_REQUEST
        )

    try:
        order = OrderItem.objects.get(pk=orderitems_entered_pk)
    except OrderItem.DoesNotExist:
        return Response(
            {"message": "order items does not exist"}, status=status.HTTP_404_NOT_FOUND
        )
    order.delete()
    return Response({"message": "order items deleted successfully"})
