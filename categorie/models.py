from django.db import models
from django.utils.text import slugify
import uuid


class Category(models.Model):

    name = models.CharField(
        max_length=100,
        unique=True
    )
    slug = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)  

    description = models.TextField(
        blank=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )


    def __str__(self):
        return self.name