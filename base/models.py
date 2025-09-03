from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.contrib.auth.base_user import BaseUserManager
from phonenumber_field.modelfields import PhoneNumberField
import datetime
from django.core.exceptions import ValidationError
from django.db.models import Prefetch, Sum

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
    phone = PhoneNumberField(region='EG' ,blank=True, null=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField(auto_now_add=True)
    
    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['full_name']

    def __str__(self):
        return f'{self.full_name} [{self.email}]'


# class Components(models.Model):
#     item = models.CharField(max_length=100)
#     salary = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)

#     def __str__(self): 
#         return f"{self.item}"

#     class Meta:
#         verbose_name_plural = "Components"


# class Cps_details(models.Model):
#     component = models.ForeignKey(Components, on_delete=models.CASCADE)
#     part_name = models.CharField(max_length=100)
#     price = models.DecimalField(max_digits=10, decimal_places=2)

#     def __str__(self):
#         return f"{self.part_name}: ${self.price:.2f}"
    
#     class Meta:
#         verbose_name_plural = "Component Details"


# class Products(models.Model):
#     name = models.CharField(max_length=100)
#     describe = models.TextField()
#     image = models.ImageField(upload_to='products/')
#     components = models.ManyToManyField(Components, blank=True)
#     created_at = models.DateTimeField(auto_now_add=True)

#     def __str__(self):
#         return self.name
    
#     @property
#     def base_price(self):
#         """Calculate base price from component salaries"""
#         return sum(
#             component.salary or 0 
#             for component in self.components.all()
#         )

class Order(models.Model):
    STATUS_CHOICES = (
        ('Pending', 'Pending'),
        ('InProgress', 'In Progress'),
        ('Completed', 'Completed'),
        ('Cancelled', 'Cancelled'),
        ('Delivered', 'Delivered'),
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    details = models.TextField()
    image = models.ImageField(upload_to='order_images/', blank=True, null=True)
    # amount = models.IntegerField(default=1)
    full_address = models.CharField(max_length=255, default='', blank=True)
    # note = models.TextField(default='', blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending')
    is_quick = models.BooleanField(default=False)
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, default=0)
    paid = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    deposit = models.IntegerField(null=True, blank=True, default=0)
    # is_paid = models.BooleanField(default=False)
    due_date = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Order {self.id} by {self.user.full_name} - {self.status}"

    # ! ------ work ---------
    @property
    def real_order_price(self):
        ''' the real price the user will pay '''
        return self.price + self.deposit
    
    @property
    def remaining_balance(self):
        """Calculate how much is still owed"""
        return self.real_order_price - self.paid
    
    @classmethod
    def get_delayed_order_balance(self):
        return self.objects.filter(paid__lt=models.F('price'))
    
    @classmethod
    def get_total_revenue(self):
        ''' get the addition for all order prices '''
        return  self.objects.aggregate(total=Sum('price'))['total'] or 0
    
    @classmethod
    def get_total_user_order_price(self, user):
        ''' addition between price and deposit in one function '''
        user_orders = self.objects.filter(user=user)
        total = 0
        for order in user_orders:
            total += order.price + order.deposit
        return total

    def clean(self):
        super().clean()
        if self.paid and self.paid > self.price:
            raise ValidationError({
                "paid": f"Paid amount ({self.paid}) cannot be bigger than the total price ({self.price})."
            })
        
        # check the numeric fields is mot none to prevent the error 
        if self.price is None:
            self.price = 0
        if self.deposit is None:
                self.deposit = 0
        if self.paid is None:
            self.paid = 0
        # if self.price and self.price is None:
        #     raise ValidationError({
        #         'price': 'you should set 0 or any number here.'})
        # if self.deposit and self.deposit is None:
        #     raise ValidationError({
        #         'deposit': 'you should set 0 or any number here.'})
        # if self.paid and self.paid is None:
        #     raise ValidationError({
        #         'paid': 'you should set 0 or any number here.'})
    class Meta:
        ordering = ['-created_at']


class OrderImages(models.Model):
    image = models.ImageField(upload_to='order_images/', null=True, blank=True)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
