from mouvement_stock.models import MouvementStock
from django.db import transaction
from .models import Inventory
from rest_framework import serializers


@transaction.atomic
def create_inventory(**validated_data):

    inventory = Inventory.objects.create(
        **validated_data
    )

    if inventory.quantity > 0:
        MouvementStock.objects.create(
            inventory=inventory,
            type='ENTREE',
            quantity=inventory.quantity,
            motif='Stock initial'
        )

    elif inventory.quantity < inventory.minimum_stock:
        raise serializers.ValidationError({
                    'quantity': 'La quantité doit être supérieure à la quantité minimum.'
        })

    elif inventory.quantity < 0 or inventory.minimum_stock < 0 :
            raise serializers.ValidationError({
                    'quantity': 'La quantité doit être supérieure a 0'
            })
    
    return inventory