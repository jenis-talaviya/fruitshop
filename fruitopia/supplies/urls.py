from django.contrib import admin
from django.urls import path, include
from .views import *

urlpatterns = [
    path("supply_list/", supply_list, name="supply_list"),
    path("supply_add/",supply_add, name="supply_add"),
    path("supply_update/",supply_update, name="supply_update"),
    path("supply_delete/",supply_delete, name="supply_delete"),
]
