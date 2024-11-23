from django.shortcuts import render
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Orders
from orders_items.models import OrderItem
from products.models import Products
from .serializers import OrdersSerializer
from django.db import transaction
from django.core.mail import send_mail
from django.conf import settings

# Create your views here.


@api_view(['POST'])
def create_order(request):
    data = request.data
    try:
        with transaction.atomic():
            # Create the order
            total_amount = 0
            for item in data['items']:
                product = Products.objects.get(id=item['product_id'])
                if product.quantity < item['quantity']:
                    return Response({"error": f"Not enough stock for product {product.id}"}, status=status.HTTP_400_BAD_REQUEST)
                total_amount += item['quantity'] * product.price
            
            # Create the order with the calculated total amount
            order = Orders.objects.create(
                customer_id=data['customer_id'],
                status=data['status'],
                total_amount=total_amount
            )
            
            # Add items to the order
            for item in data['items']:
                product = Products.objects.get(id=item['product_id'])
                OrderItem.objects.create(
                    order=order,
                    product=product,
                    quantity=item['quantity'],
                    price=product.price  # Use product price from the database
                )
                
                # product.quantity -= item['quantity']
                # product.save()
            
            return Response({"order_id": order.id, "total_amount": total_amount}, status=status.HTTP_201_CREATED)
    except Products.DoesNotExist:
        return Response({"error": "One or more products not found"}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)





@api_view(["POST"])
def order_add(request):
        serializer = OrdersSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET"])
def order_list(request):
    order = Orders.objects.all()
    serializer = OrdersSerializer(order, many=True)
    return Response(serializer.data)



@api_view(["PUT"])
def order_update(request):
    order_entered_pk = request.headers.get("pk1")
    if not order_entered_pk:
        return Response(
            {"error": "PK header is required"}, status=status.HTTP_400_BAD_REQUEST
        )

    try:
        order = Orders.objects.get(pk=order_entered_pk)
    except Orders.DoesNotExist:
        return Response(
            {"message": "order does not exist"}, status=status.HTTP_404_NOT_FOUND
        )
        
    serializer = OrdersSerializer(order, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({"message": "Detail updated successfully", "data": serializer.data},status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



@api_view(["PUT"])
def order_status_update(request):
    order_entered_pk = request.headers.get("pk1")
    if not order_entered_pk:
        return Response(
            {"error": "PK header is required"}, status=status.HTTP_400_BAD_REQUEST
        )

    try:
        order = Orders.objects.get(pk=order_entered_pk)
    except Orders.DoesNotExist:
        return Response(
            {"message": "Order does not exist"}, status=status.HTTP_404_NOT_FOUND
        )
    
    # Check if the status is being updated to 'confirmed'
    status_updated = request.data.get('status')
    serializer = OrdersSerializer(order, data=request.data, partial=True)
    
    if serializer.is_valid():
        serializer.save()
        
        if status_updated == 'confirmed':
            # Send email notification to the customer
            customer_email = order.customer.email
            send_order_confirmation_email(customer_email)
        
        return Response(
            {"message": "Detail updated successfully", "data": serializer.data},
            status=status.HTTP_200_OK
        )
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

def send_order_confirmation_email(email):
    subject = 'Order Confirmation'
    message = 'Your order has been received successfully and is being processed.'
    from_email = settings.DEFAULT_FROM_EMAIL
    send_mail(subject, message, from_email, [email])



@api_view(["DELETE"])
def order_delete(request):
    order_entered_pk = request.headers.get("pk1")
    if not order_entered_pk:
        return Response(
            {"error": "PK header is required"}, status=status.HTTP_400_BAD_REQUEST
        )

    try:
        order = Orders.objects.get(pk=order_entered_pk)
    except Orders.DoesNotExist:
        return Response(
            {"message": "category does not exist"}, status=status.HTTP_404_NOT_FOUND
        )
    order.delete()
    return Response({"message": "category deleted successfully"})
