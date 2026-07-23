from django.db import transaction
from rest_framework.exceptions import ValidationError

from inventory.models import Inventory
from .models import MouvementStock


@transaction.atomic
def create_stock_movement(
    inventory_id,
    movement_type,
    quantity,
    motif=None
):
    inventory = (
        Inventory.objects
        .select_for_update()
        .get(id=inventory_id)
    )

    if movement_type == 'SORTIE':

        if quantity > inventory.quantity:
            raise ValidationError({
                'quantity': 'Stock insuffisant.'
            })

        inventory.quantity -= quantity

    elif movement_type == 'ENTREE':

        inventory.quantity += quantity

    elif movement_type == 'AJUSTEMENT':

        if quantity > inventory.quantity:
            raise ValidationError({
                'quantity': (
                    'La valeur ajustée est supérieure '
                    'à la quantité actuelle.'
                )
            })

        inventory.quantity -= quantity

    else:
        raise ValidationError({
            'type': 'Type de mouvement invalide.'
        })

    inventory.save(
        update_fields=['quantity']
    )

    mouvement = MouvementStock.objects.create(
        inventory=inventory,
        type=movement_type,
        quantity=quantity,
        motif=motif
    )

    return mouvement