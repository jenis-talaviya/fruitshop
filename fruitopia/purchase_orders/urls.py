from django.contrib import admin
from django.urls import path, include
from .views import *

urlpatterns = [
    path("purchaseorder_list/", purchaseorder_list, name="purchaseorder_list"),
    path("purchaseorder_add/",purchaseorder_add, name="purchaseorder_add"),
    path("purchaseorder_update/",purchaseorder_update, name="purchaseorder_update"),
    path("purchaseorder_delete/",purchaseorder_delete, name="purchaseorder_delete"),
]
