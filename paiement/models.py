from django.db import models
import uuid
from commande.models import Commande


class Paiement(models.Model):

    MOYEN_CHOICES = (
        ('MTN', 'MTN Mobile Money'),
        ('ORANGE', 'Orange Money'),
    )


    STATUT_CHOICES = (
        ('EN_ATTENTE', 'En attente'),
        ('REUSSI', 'Réussi'),
        ('ECHOUE', 'Échoué'),
    )


    commande = models.OneToOneField(
        Commande,
        on_delete=models.CASCADE,
        related_name="paiement"
    )


    reference = models.UUIDField(
        default=uuid.uuid4,
        unique=True,
        editable=False
    )


    montant = models.PositiveBigIntegerField()


    moyen = models.CharField(
        max_length=20,
        choices=MOYEN_CHOICES
    )


    statut = models.CharField(
        max_length=20,
        choices=STATUT_CHOICES,
        default="EN_ATTENTE"
    )


    created_at = models.DateTimeField(
        auto_now_add=True
    )


    def __str__(self):
        return f"{self.reference} - {self.statut}"