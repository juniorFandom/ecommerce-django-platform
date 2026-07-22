from django.db import transaction
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
            raise ValueError("Stock insuffisant.")

        inventory.quantity -= quantity

    elif movement_type == 'ENTREE':
        inventory.quantity += quantity

    inventory.save()

    return MouvementStock.objects.create(
        inventory=inventory,
        type=movement_type,
        quantity=quantity,
        motif=motif
    )