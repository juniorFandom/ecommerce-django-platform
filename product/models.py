from django.db import models
from categorie.models import Category
from django.utils.text import slugify
import uuid


class Product(models.Model):
    category = models.ForeignKey(
        Category,
        on_delete=models.PROTECT,
        related_name='products'
    )
    name = models.CharField(max_length=100)
    prix = models.DecimalField(max_digits=10, decimal_places=2)
    is_active = models.BooleanField(default=True)
    slug = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)  

    class Meta:
        verbose_name = 'Product'
        verbose_name_plural = 'Products'
        ordering = ['-pk']

    def is_active(self):
        return self.is_active
    
    def __str__(self):
        return self.name
    
