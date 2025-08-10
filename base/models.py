from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.contrib.auth.base_user import BaseUserManager
from phonenumber_field.modelfields import PhoneNumberField

class UserManager(BaseUserManager):
    def create_user(self, email, full_name, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, full_name=full_name, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, full_name, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, full_name, password, **extra_fields)

class User(AbstractBaseUser, PermissionsMixin):
    full_name = models.CharField(max_length=100, blank=False)
    email = models.EmailField(unique=True)
    phone = PhoneNumberField(blank=True, null=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField(auto_now_add=True)
    
    objects = UserManager()
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['full_name']

    def __str__(self):
        return self.email



class Address(models.Model):
    full_address = models.CharField(max_length=255)



class Components(models.Model):
    item = models.CharField(max_length=100)
    salary = models.DecimalField(max_digits=10, decimal_places=2, default=0.00, blank=True)

    def __str__(self): 
        return f"{self.item}"


class Cps_details(models.Model):
    component = models.ForeignKey(Components, on_delete=models.CASCADE)
    part_name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.part_name}: ${self.price:.2f}"
    

class Products(models.Model):
    name = models.CharField(max_length=100)
    describe = models.TextField()
    image = models.ImageField(upload_to='products/')
    # many to many relationship with Components, because a product can have multiple components and a component can belong to multiple products
    components = models.ManyToManyField(Components, blank=True)

    # TODO: get total price of product based on components
    def __str__(self):
        return self.name


class Order(models.Model):
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    )

    product = models.ForeignKey(Products, on_delete=models.CASCADE)
    components = models.ManyToManyField(Components, blank=True)
    components_details = models.ManyToManyField(Cps_details, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.IntegerField(default=1)
    address = models.ForeignKey(Address, on_delete=models.SET_NULL, null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    paid = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    due_date = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Order {self.id} by {self.user.name} - {self.status}"
