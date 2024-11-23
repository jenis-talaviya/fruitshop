from django.contrib import admin
from django.urls import path, include
from .views import *

urlpatterns = [
    path("category_add/", category_add, name="category_add"),
    path("category_list/", category_list, name="category_list"),
    path("category_update/", category_update, name="category_update"),
    path("category_delete/", category_delete, name="category_delete"),
]