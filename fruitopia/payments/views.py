from django.shortcuts import render
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Orders,Payment
from .serializers import PaymentsSerializer
from django.core.mail import send_mail
from django.conf import settings
# Create your views here.

# @api_view(["POST"])
# def payment_add(request):
#         serializer = PaymentsSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)


@api_view(["POST"])
def payment_add(request):
    serializer = PaymentsSerializer(data=request.data)
    if serializer.is_valid():
        payment = Payment(
            order=serializer.validated_data['order'],
            method=serializer.validated_data['method'],
            status=serializer.validated_data['status'],
            customer=serializer.validated_data['customer']
        )

        # Calculate amount based on the associated order
        order = payment.order
        payment.amount = order.total_amount  # Assuming 'total_amount' is a field in Orders model
        payment.save()

        # Check if the payment method is 'COD'
        if payment.method.upper() == 'COD':
            payment.status = 'Done'
            payment.save()

            # Send email notification to the customer
            send_mail(
                'Payment Received',
                f'Your payment for Order {order.id} has been received successfully.',
                settings.DEFAULT_FROM_EMAIL,
                [payment.customer.email],
                fail_silently=False,
            )

        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



@api_view(["GET"])
def payment_list(request):
    payment = Payment.objects.all()
    serializer = PaymentsSerializer(payment, many=True)
    return Response(serializer.data)



@api_view(["PUT"])
def payment_update(request):
    payment_entered_pk = request.headers.get("pk1")
    if not payment_entered_pk:
        return Response(
            {"error": "PK header is required"}, status=status.HTTP_400_BAD_REQUEST
        )

    try:
        payment = Orders.objects.get(pk=payment_entered_pk)
    except Orders.DoesNotExist:
        return Response(
            {"message": "order does not exist"}, status=status.HTTP_404_NOT_FOUND
        )
        
    serializer = PaymentsSerializer(payment, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({"message": "Detail updated successfully", "data": serializer.data},status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



@api_view(["DELETE"])
def payment_delete(request):
    payment_entered_pk = request.headers.get("pk1")
    if not payment_entered_pk:
        return Response(
            {"error": "PK header is required"}, status=status.HTTP_400_BAD_REQUEST
        )

    try:
        payment = Orders.objects.get(pk=payment_entered_pk)
    except Orders.DoesNotExist:
        return Response(
            {"message": "payment does not exist"}, status=status.HTTP_404_NOT_FOUND
        )
    payment.delete()
    return Response({"message": "payment deleted successfully"})
