from django.contrib import admin
from django.urls import path, include
from .views import *

urlpatterns = [
    path("orderitems_list/", orderitems_list, name="orderitems_list"),
    path("orderitems_add/",orderitems_add, name="orderitems_add"),
    path("orderitems_update/",orderitems_update, name="orderitems_update"),
    path("orderitems_delete/",orderitems_delete, name="orderitems_delete"),
]
