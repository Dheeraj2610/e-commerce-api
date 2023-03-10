from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class registration(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    User_Name = models.CharField(max_length=50, null=False)
    Email = models.EmailField(unique=True, null=False)
    Password = models.CharField(max_length=100)
    def __str__(self):
        return self.User_Name
    
class Category(models.Model):
    name = models.CharField(max_length=255)
    
    def __str__(self):
        return self.name
    
class Product(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    discount = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    offer_start_date = models.DateField(blank=True, null=True)
    offer_end_date = models.DateField(blank=True, null=True)
     
    def __str__(self):
        return self.name
    
class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    products = models.ForeignKey(Product,on_delete=models.CASCADE)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)

class CartItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    class Meta:
        unique_together = ('user', 'product',)


class Contact(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    address = models.CharField(max_length=255)