from django.contrib import admin
from django.urls import path, include
from .views import *

urlpatterns = [
    path("order_list/", order_list, name="order_list"),
    path("order_add/",order_add, name="order_add"),
    path("order_update/",order_update, name="order_update"),
    path("order_status_update/",order_status_update, name="order_status_update"),
    path("order_delete/",order_delete, name="order_delete"),
    path("create_order/",create_order, name="create_order"),
]
