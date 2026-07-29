from django.db import models
from product.models import Product
from users.models import User
import uuid

class Commande(models.Model):

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user')
    slug = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    add_date = models.DateTimeField(auto_now=True)
    montant = models.PositiveBigIntegerField(default=0)

    
    class Meta:
        verbose_name = 'Commande'
        verbose_name_plural = 'Commandes'
        ordering = ['-add_date']

    def __str__(self):
        return f"{self.product.name}========{self.quantity}"



class LigneCommande(models.Model):
    commande = models.ForeignKey(Commande, on_delete=models.CASCADE, related_name='lignes')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='products')
    slug = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)  
    add_date = models.DateTimeField(auto_now=True)
    quantity = models.PositiveIntegerField()


    class Meta:
        verbose_name = 'LigneCommande'
        verbose_name_plural = 'LignesCommande'
        ordering = ['-add_date']

    def __str__(self):
        return f'{self.product.name}========{self.quantity}'
    
    @property
    def prix_total(self):
        return self.product.prix * self.quantity