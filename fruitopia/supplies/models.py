from django.db import models

from suppliers.models import Supplier
from products.models import Products
import uuid
# Create your models here.

class Supply(models.Model):
    id = models.UUIDField(primary_key=True)
    supplier = models.ForeignKey(Supplier, related_name='supplies', on_delete=models.CASCADE)
    product = models.ForeignKey(Products, related_name='supplies', on_delete=models.CASCADE)
    quantity = models.IntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    delivery_date = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)
    is_deleted = models.BooleanField(default=False)

    def __str__(self):
        return f'Supply of {self.product.name} by {self.supplier.name}'