from django.contrib import admin
from django.urls import path, include
from .views import *

urlpatterns = [
    path("supplier_list/", supplier_list, name="supplier_list"),
    path("supplier_add/",supplier_add, name="supplier_add"),
    path("supplier_update/",supplier_update, name="supplier_update"),
    path("supplier_delete/",supplier_delete, name="supplier_delete"),
]
