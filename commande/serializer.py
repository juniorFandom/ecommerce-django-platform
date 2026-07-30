from django.db import transaction
from rest_framework import serializers

from .models import LigneCommande, Commande
from inventory.models import Inventory


class LigneCommandeSerializer(serializers.ModelSerializer):

    class Meta:
        model = LigneCommande

        fields = [
            'id',
            'commande',
            'product',
            'quantity',
            'slug'
        ]

        read_only_fields = [
            'id',
            'commande',
            'slug'
        ]






class CommandeSerializer(serializers.ModelSerializer):

    lignes = LigneCommandeSerializer(
        many=True,
        write_only=True
    )


    class Meta:

        model = Commande

        fields = [
            'id',
            'user',
            'montant',
            'lignes',
            'slug',
            'statut'
        ]

        read_only_fields = [
            'id',
            'user',
            'montant',
            'slug',
            'statut'
        ]



    @transaction.atomic
    def create(self, validated_data):

        lignes_data = validated_data.pop('lignes')

        request = self.context.get('request')

        if request is None:
            raise serializers.ValidationError(
                "Impossible de déterminer l'utilisateur."
            )

        commande = Commande.objects.create(
            user=request.user,
            montant=0,
            **validated_data
        )

        montant = 0

        for ligne_data in lignes_data:
            product = ligne_data['product']
            quantity = ligne_data['quantity']

            inventory = Inventory.objects.select_for_update().get(
                product=product
            )

            if quantity > inventory.available_quantite:
                raise serializers.ValidationError({
                    'quantity': 'Le stock disponible est insuffisant.'
                })

            inventory.reserved_quantity += quantity
            inventory.save(update_fields=['reserved_quantity'])

            ligne = LigneCommande.objects.create(
                commande=commande,
                product=product,
                quantity=quantity
            )

            montant += ligne.prix_total

        commande.montant = montant
        commande.save(update_fields=['montant'])

        return commande