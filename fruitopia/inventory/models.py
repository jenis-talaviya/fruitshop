from django.db import models

from products.models import Products
import uuid
# Create your models here.

class Inventory(models.Model):
    id = models.UUIDField(primary_key=True,default=uuid.uuid4)
    product = models.ForeignKey(Products, related_name='inventory', on_delete=models.CASCADE)
    quantity = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)
    is_deleted = models.BooleanField(default=False)

    def __str__(self):
        return f'Inventory for {self.product.name}'