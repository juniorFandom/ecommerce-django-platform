from django.db import models
from commande.models import Commande
import uuid

class Facture(models.Model):
    commande = models.OneToOneField(Commande, on_delete=models.CASCADE, related_name='facture')
    numero = models.UUIDField(default=uuid.uuid4, editable=False, unique = True)
    montant = models.PositiveIntegerField()
    

    class Meta:
        ordering = ['-pk']

    def __str__(self):
        return f"facture {self.numero} de la commade {self.commande.pk} avec le montant {self.montant}"