from django.db import models
from inventory.models import Inventory
from django.utils.text import slugify
import uuid

class MouvementStock(models.Model):

    TYPE_MOUVEMENT = [
        ('ENTREE', 'Entrée'),
        ('SORTIE', 'Sortie'),
        ('AJUSTEMENT', 'Ajustement')
    ]

    inventory = models.ForeignKey(
        Inventory,
        on_delete=models.PROTECT,
        related_name='mouvements'
    )

    type = models.CharField(
        max_length=20,
        choices=TYPE_MOUVEMENT
    )

    quantity = models.PositiveIntegerField()

    date = models.DateTimeField(
        auto_now_add=True
    )

    motif = models.CharField(
        max_length=255,
        blank=True
    )

    slug = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)  

    def __str__(self):
        return f"{self.type} - {self.quantity}"


             