from django.db import models
from django.contrib.auth.models import User

class Category(models.Model):
    cat_name = models.CharField(max_length=255)
    cat_description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.cat_name

class Product(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.IntegerField()
    seller = models.ForeignKey(User, on_delete=models.CASCADE, related_name='products')
    image = models.ImageField(upload_to='media/uploads/', null=True, blank=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products')  # Corrected field name

    def __str__(self):
        return self.name

class CartItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    buyer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='cart_items')

    def __str__(self):
        return f"{self.product.name} ({self.quantity})"

class Order(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    products = models.ManyToManyField(Product, through='OrderProduct')
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    buyer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders')

    def save(self, *args, **kwargs):
        self.total_price = sum(item.product.price * item.quantity for item in self.orderproduct_set.all())
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Order {self.id}"

class OrderProduct(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField()
