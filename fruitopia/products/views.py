from django.shortcuts import render

# Create your views here.
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Products
from .serializers import ProductSerializer


@api_view(["POST"])
def product_add(request):
        serializer = ProductSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)



@api_view(["GET"])
def product_list(request):
    product = Products.objects.all()
    serializer = ProductSerializer(product, many=True)
    return Response(serializer.data)



@api_view(["PUT"])
def product_update(request):
    product_entered_pk = request.headers.get("pk1")
    if not product_entered_pk:
        return Response(
            {"error": "PK header is required"}, status=status.HTTP_400_BAD_REQUEST
        )

    try:
        product = Products.objects.get(pk=product_entered_pk)
    except Products.DoesNotExist:
        return Response(
            {"message": "product does not exist"}, status=status.HTTP_404_NOT_FOUND
        )
        
    serializer = ProductSerializer(product, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({"message": "Detail updated successfully", "data": serializer.data},status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



@api_view(["DELETE"])
def product_delete(request):
    product_entered_pk = request.headers.get("pk1")
    if not product_entered_pk:
        return Response(
            {"error": "PK header is required"}, status=status.HTTP_400_BAD_REQUEST
        )

    try:
        product = Products.objects.get(pk=product_entered_pk)
    except Products.DoesNotExist:
        return Response(
            {"message": "product does not exist"}, status=status.HTTP_404_NOT_FOUND
        )
    product.delete()
    return Response({"message": "product deleted successfully"})
