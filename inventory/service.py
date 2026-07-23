from mouvement_stock.models import MouvementStock
from django.db import transaction
from .models import Inventory


@transaction.atomic
def create_inventory(validated_data):

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

    return inventory