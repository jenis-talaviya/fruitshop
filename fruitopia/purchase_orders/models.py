from django.db import models

from suppliers.models import Supplier
import uuid
# Create your models here.

class PurchaseOrder(models.Model):
    id = models.UUIDField(primary_key=True,default=uuid.uuid4)
    supplier = models.ForeignKey(Supplier, related_name='purchase_orders', on_delete=models.CASCADE)
    order_date = models.DateTimeField()
    status = models.CharField(max_length=50)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)
    is_deleted = models.BooleanField(default=False)


    def __str__(self):
        return f'Purchase Order {self.id} by {self.supplier.name}'