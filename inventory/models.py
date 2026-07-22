from django.db import models
from product.models import Product
from django.utils.text import slugify

class Inventory(models.Model):
    product = models.OneToOneField(Product, on_delete=models.CASCADE, related_name='inventory')
    quantity = models.PositiveIntegerField(default=0)
    last_updated = models.DateTimeField(auto_now=True)
    reserved_quantity = models.PositiveIntegerField(default=0)

    minimum_stock = models.PositiveIntegerField( default=5)
    slug = models.SlugField(max_length=100, unique=True, blank=True)

    class Meta:
        verbose_name = 'Inventory'
        verbose_name_plural = 'Inventories'
        ordering = ['-last_updated']

    def __str__(self):
        return f"{self.product.name} - {self.quantity}"

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.product.name)
            slug = base_slug
            counter = 1
            while Inventory.objects.filter(slug=slug).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            self.slug = slug

        super().save(*args, **kwargs)

    @property
    def available_quantity(self):
        return (self.quantity - self.reserved_quantity)>0