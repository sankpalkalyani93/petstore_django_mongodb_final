from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator

# Create your models here.   
class CustomUser(AbstractUser):
    phone_number = models.CharField(max_length=20)


class Pet(models.Model):
    id = models.AutoField(primary_key=True)
    category = models.CharField(max_length=100)
    name = models.CharField(max_length=50)
    breed = models.CharField(max_length=100)
    price = models.IntegerField()
    image = models.ImageField(upload_to='pet_images/', null=True, blank=True)

    def __str__(self):
        return f"{ self.name }"

class Product(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    price = models.IntegerField()
    category = models.CharField(max_length=100)
    quantity = models.IntegerField()
    image = models.ImageField(upload_to='product_images/', null=True, blank=True)

    def __str__(self):
        return f"{ self.name }"
    
class Cart(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    #user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Cart for {self.user.username}"

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    pet = models.ForeignKey(Pet, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(validators=[MinValueValidator(1)])

    def __str__(self):
        return f"{self.quantity} x {self.pet.name} in cart for {self.cart.user.username}"


