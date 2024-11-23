from django.shortcuts import render
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Categories
from .serializers import CategoriesSerializer

# Create your views here.

@api_view(["POST"])
def category_add(request):
        serializer = CategoriesSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET"])
def category_list(request):
    category = Categories.objects.all()
    serializer = CategoriesSerializer(category, many=True)
    return Response(serializer.data)



@api_view(["PUT"])
def category_update(request):
    category_entered_pk = request.headers.get("pk1")
    if not category_entered_pk:
        return Response(
            {"error": "PK header is required"}, status=status.HTTP_400_BAD_REQUEST
        )

    try:
        category = Categories.objects.get(pk=category_entered_pk)
    except Categories.DoesNotExist:
        return Response(
            {"message": "category does not exist"}, status=status.HTTP_404_NOT_FOUND
        )
        
    serializer = CategoriesSerializer(category, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({"message": "Detail updated successfully", "data": serializer.data},status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



@api_view(["DELETE"])
def category_delete(request):
    category_entered_pk = request.headers.get("pk1")
    if not category_entered_pk:
        return Response(
            {"error": "PK header is required"}, status=status.HTTP_400_BAD_REQUEST
        )

    try:
        category = Categories.objects.get(pk=category_entered_pk)
    except Categories.DoesNotExist:
        return Response(
            {"message": "category does not exist"}, status=status.HTTP_404_NOT_FOUND
        )
    category.delete()
    return Response({"message": "category deleted successfully"})
