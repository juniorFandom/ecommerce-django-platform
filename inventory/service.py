from mouvement_stock.models import MouvementStock
from django.db import transaction
from .models import Inventory
from rest_framework import serializers


@transaction.atomic
def create_inventory(**validated_data):

    print("creation de l'inventaire:________")
    inventory = Inventory.objects.create(
        **validated_data
    )

    print("comparaison de la quantity avec la quantit mininum")
    if inventory.quantity < inventory.minimum_stock:
        print("la quantite est inferieur a 0, annulation des actions")

        raise serializers.ValidationError({
                    'quantity': 'La quantité doit être supérieure à la quantité minimum.'
        })

    elif inventory.quantity < 0 or inventory.minimum_stock < 0 :
            print("une valeur negative")
            raise serializers.ValidationError({
                    'quantity': 'La quantité doit être supérieure a 0'
            })
    
    elif inventory.quantity > 0:
        print("la quantite est superieure a 0")
        print(f"creation du mouvement de stock {inventory.pk},{inventory.quantity}")
        MouvementStock.objects.create(
            inventory=inventory,
            type='ENTREE',
            quantity=inventory.quantity,
            motif='Stock initial'
        )


    
    return inventory