from django.db import models
from product.models import Product
from django.utils.text import slugify
import uuid

class Inventory(models.Model):
    product = models.OneToOneField(Product, on_delete=models.CASCADE, related_name='inventory')
    quantity = models.PositiveIntegerField(default=0)
    last_updated = models.DateTimeField(auto_now=True)
    reserved_quantity = models.PositiveIntegerField(default=0)

    minimum_stock = models.PositiveIntegerField( default=5)
    slug = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)  

    class Meta:
        verbose_name = 'Inventory'
        verbose_name_plural = 'Inventories'
        ordering = ['-last_updated']

    def __str__(self):
        return f"{self.product.name} - {self.quantity}"

   

    @property
    def available_quantity(self):
        return (self.quantity - self.reserved_quantity)>0