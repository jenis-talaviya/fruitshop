from django.contrib import admin
from django.urls import path, include
from .views import *

urlpatterns = [
    path("inventory_list/", inventory_list, name="inventory_list"),
    path("inventory_add/",inventory_add, name="inventory_add"),
    path("inventory_update/",inventory_update, name="inventory_update"),
    path("inventory_delete/",inventory_delete, name="inventory_delete"),
]
