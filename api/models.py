import uuid
from django.db import models
from django.contrib.auth.models import User

class Product(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField()
    image = models.ImageField(upload_to='products/', blank=True, null=True)

    @property
    def in_stock(self):
        return self.stock > 0
    
    def __str__(self):
        return self.name
    
class Order(models.Model):
    class Status_Choise(models.TextChoices):
        PENDING = 'Pending'
        CONFIRMED = 'Confirmed'
        CANCELLED = 'Cancelled'

    order_id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_ad = models.DateTimeField(auto_now_add=True)
    products = models.ManyToManyField(Product, through='OrderItem', related_name='order')
    status = models.CharField(max_length=10, choices=Status_Choise.choices, default=Status_Choise.PENDING)

    def __str__(self):
        return f"Order {self.order_id} by {self.user.username}"
    
class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quentity = models.PositiveIntegerField()

    @property
    def item_subtotal(self):
        return self.product.price * self.quentity
    
    def __str__(self):
        return f"{self.quentity} x {self.product.name} Order No {self.order.order_id}"