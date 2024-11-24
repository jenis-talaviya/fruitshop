from django.shortcuts import render
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Customers
from .serializers import CustomerSerializer,CustomerSerializerGet
from rest_framework.exceptions import ValidationError
from .models import BlacklistedToken

# Create your views here.

@api_view(["GET"])
def customer_list(request):
    customers = Customers.objects.all()
    serializer = CustomerSerializerGet(customers, many=True)
    return Response(serializer.data)


    
@api_view(["POST"])
def customer_add(request):
        serializer = CustomerSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)



@api_view(["POST"])
def customer_logout(request):
    try:
        access_token = request.data.get('access_token')
        
        if not access_token:
            return Response({"error": "Access token is required"}, status=status.HTTP_400_BAD_REQUEST)

        # Check if the token is already blacklisted
        if BlacklistedToken.objects.filter(token=access_token).exists():
            return Response({"message": "Token already blacklisted"}, status=status.HTTP_400_BAD_REQUEST)

        # Blacklist the token
        BlacklistedToken.objects.create(
            token=access_token,
            blacklisted_at=timezone.now()
        )

        return Response({"message": "Logout successful"}, status=status.HTTP_200_OK)

    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
    
    

@api_view(["PUT"])
def customer_update(request):
    user_entered_pk = request.headers.get("pk1")
    if not user_entered_pk:
        return Response(
            {"error": "PK header is required"}, status=status.HTTP_400_BAD_REQUEST
        )

    try:
        custom = Customers.objects.get(pk=user_entered_pk)
    except Customers.DoesNotExist:
        return Response(
            {"message": "customer does not exist"}, status=status.HTTP_404_NOT_FOUND
        )
        
    serializer = CustomerSerializer(custom, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({"message": "Detail updated successfully", "data": serializer.data},status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



@api_view(["DELETE"])
def customer_delete(request):
    user_entered_pk = request.headers.get("pk1")
    if not user_entered_pk:
        return Response(
            {"error": "PK header is required"}, status=status.HTTP_400_BAD_REQUEST
        )

    try:
        custom = Customers.objects.get(pk=user_entered_pk)
    except Customers.DoesNotExist:
        return Response(
            {"message": "customer does not exist"}, status=status.HTTP_404_NOT_FOUND
        )
    custom.delete()
    return Response({"message": "customer deleted successfully"})



#---------------------------------OTP API-----------------------------------------


from rest_framework.exceptions import NotFound, ValidationError
from django.utils import timezone
from datetime import timedelta
from .models import Customers, Otp
from fruitopia.settings import generate_otp, send_otp_via_email, get_token, decode_token_user_id, decode_token_user_email, decode_token_password
from django.contrib.auth.hashers import make_password, check_password


@api_view(["POST"])
def generate_otp_for_user(request):
    email = request.data.get('email')
    db_user = Customers.objects.filter(email=email, is_active=True).first()
    if not db_user:
        raise NotFound("Email is not registered")

    otp_code = generate_otp()
    expiry_time = timezone.now() + timedelta(minutes=10)  # OTP valid for 10 minutes
    new_otp = Otp(email=email, otp=otp_code, expiry_time=expiry_time)
    new_otp.save()

    # Send OTP via email
    sender_email = "jenistalaviya404@gmail.com"
    receiver_email = email
    email_password = "your password"
    success, message = send_otp_via_email(sender_email, receiver_email, email_password, otp_code)

    if not success:
        raise ValidationError("OTP can't be sent")

    return Response({"message": "OTP sent to email", "email": email})



@api_view(["POST"])
def verify_otp(request):
    email = request.data.get('email')
    otp = request.data.get('otp')
    db_record = Otp.objects.filter(email=email, otp=otp).first()
    if not db_record:
        raise ValidationError("Invalid Entered OTP")

    if timezone.now() > db_record.expiry_time:
        raise ValidationError("OTP has expired")

    user_record = Customers.objects.filter(email=email).first()
    if not user_record:
        raise NotFound("Email is not found")

    # Update the is_verified field in the CustomerDetail table
    user_record.is_verify = True
    user_record.save()

    # Delete OTP after verification
    db_record.delete()

    return Response({"message": "OTP verified successfully"})



@api_view(["POST"])
def logging_user(request):
    email = request.data.get('email')
    password = request.data.get('password')
    db_user = Customers.objects.filter(
        email=email, is_active=True, is_deleted=False, is_verify=True
    ).first()

    if not db_user:
        raise NotFound("customer is not found")

    if not check_password(password, db_user.password):
        raise ValidationError("Password is incorrect")

    # Generate the access token
    access_token = get_token(str(db_user.id), email, password)
    return Response({"access_token": str(access_token)})



@api_view(["PUT"])
def reset_password(request):
    newpass = request.data.get('newpass')
    token = request.data.get('token')
    id = decode_token_user_id(token)
    email = decode_token_user_email(token)
    password = decode_token_password(token)

    db_user = Customers.objects.filter(id=id, email=email, is_active=True).first()
    if not db_user:
        raise NotFound("Customer data is not found")

    if check_password(password, db_user.password):
        db_user.password = make_password(newpass)
        db_user.save()
        return Response({"message": "Password reset successfully"})
    else:
        raise ValidationError("Old password does not match")



@api_view(["PUT"])
def reregister_user(request):
    email = request.data.get('email')
    password = request.data.get('password')
    token = request.headers.get('Authorization')
    
    if not token:
        raise ValidationError("Token is missing from headers")
    
    id = decode_token_user_id(token)

    db_user = Customers.objects.filter(id=id).first()
    if not db_user:
        raise NotFound("Customer not found")

    if not db_user.is_active and db_user.is_deleted:
        if check_password(password, db_user.password):
            db_user.is_active = True
            db_user.is_deleted = False
            db_user.save()
            return Response({"message": "Successfully re-registered"})
    else:
        raise ValidationError("Email or password does not match")



@api_view(["PUT"])
def forget_password(request):
    user_newpass = request.data.get('user_newpass')
    token = request.data.get('token')
    user_id = decode_token_user_id(token)

    db_user = Customers.objects.filter(
        id=user_id, is_active=True, is_verify=True, is_deleted=False
    ).first()

    if not db_user:
        raise NotFound("customer not found")

    if not db_user.is_verify:
        raise ValidationError("customer is not verified")

    db_user.password = make_password(user_newpass)
    db_user.save()
    return Response({"message": "Password reset successfully"})