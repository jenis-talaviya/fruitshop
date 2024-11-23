from django.contrib import admin
from django.urls import path, include
from .views import *

urlpatterns = [
    path("customer_list/", customer_list, name="customer_list"),
    path("customer_add/",customer_add, name="customer_add"),
    path("customer_update/",customer_update, name="customer_update"),
    path("customer_delete/",customer_delete, name="customer_delete"),
    path("generate_otp_for_user/",generate_otp_for_user, name ="generate_otp_for_user"),
    path("verify_otp/",verify_otp, name ="verify_otp"),
    path("logging_user/",logging_user, name ="logging_user"),
    path("customer_logout/",customer_logout, name ="customer_logout"),
    path("reregister_user/",reregister_user, name ="reregister_user"),
    path("forget_password/",forget_password, name ="forget_password"),
    path("reset_password/",reset_password, name ="reset_password"),
]
