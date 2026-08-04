from django.contrib.auth.models import AbstractUser
from django.db import models
import uuid


class User(AbstractUser):

    ROLE_CHOICES = [
        ('ADMIN', 'Administrateur'),
        ('GESTIONNAIRE', 'Gestionnaire'),
        ('VENDEUR', 'Vendeur'),
        ('CLIENT', 'Client'),
    ]

    role = models.CharField(
        max_length=20,
        choices=ROLE_CHOICES,
        default='CLIENT'
    )
    email = models.EmailField(
        unique=True
    )

    phone = models.PositiveBigIntegerField(default=655318272)


    slug = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)  

    def __str__(self):
        return self.username

    def check_user_active(self):
        return self.is_active