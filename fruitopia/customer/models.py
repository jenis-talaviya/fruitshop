from django.db import models
import uuid
from django.contrib.auth.hashers import make_password
from django.utils import timezone
# Create your models here.

class Customers(models.Model):
    id = models.UUIDField(primary_key=True,default=uuid.uuid4,editable=False)
    fname = models.CharField(max_length=100)
    lname = models.CharField(max_length=100)
    address = models.TextField()
    phone = models.CharField(max_length=15)
    email = models.EmailField()
    password = models.CharField(max_length=128,  default=make_password('temporarypassword'))
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)
    is_deleted = models.BooleanField(default=False)
    is_verify = models.BooleanField(default=False)
    
    def __str__(self):
        return self.fname,self.lname
    
    def save(self, *args, **kwargs):
        # Hash the password with bcrypt before saving
        if self.password and not self.password.startswith('pbkdf2_'):
            self.password = make_password(self.password)
        super(Customers, self).save(*args, **kwargs)



class BlacklistedToken(models.Model):
    token = models.CharField(max_length=255)
    blacklisted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.token



class Otp(models.Model):
    id = models.UUIDField(primary_key=True,default=uuid.uuid4,editable=False)
    email = models.EmailField()
    otp = models.CharField(max_length=6)
    expiry_time = models.DateTimeField(default=timezone.now)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return str(self.email)