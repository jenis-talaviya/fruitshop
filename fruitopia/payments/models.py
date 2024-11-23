from django.db import models

from orders.models import Orders
from customer.models import Customers
import uuid
# Create your models here.

class Payment(models.Model):
    id = models.UUIDField(primary_key=True,default=uuid.uuid4,editable=False)
    order = models.ForeignKey(Orders, related_name='payments', on_delete=models.CASCADE)
    customer = models.ForeignKey(Customers, related_name='payments', on_delete=models.CASCADE,null=True)
    payment_date = models.DateTimeField(auto_now_add=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    method = models.CharField(max_length=50)
    status = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)
    is_deleted = models.BooleanField(default=False)
    
    
    def __str__(self):
        return f'Payment for Order {self.order.id}'