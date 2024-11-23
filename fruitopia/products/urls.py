from django.contrib import admin
from django.urls import path, include
from .views import *

urlpatterns = [
    path("product_list/", product_list, name="product_list"),
    path("product_add/",product_add, name="product_add"),
    path("product_update/",product_update, name="product_update"),
    path("product_delete/",product_delete, name="product_delete"),
]
