from rest_framework import serializers
from .models import MouvementStock
from .service import create_stock_movement
from inventory.serializer import InventorySerializer

class MouvementStockSerializer(serializers.ModelSerializer):

    class Meta:
        model = MouvementStock
        fields = [
            'inventory',
            'type',
            'quantity',
            'motif',
            'slug'
        ]
        read_only_fields =['slug']

    def validate_quantity(self, value):

        if value <= 0:
            raise serializers.ValidationError(
                "La quantité doit être supérieure à zéro."
            )

        return value

    def create(self, validated_data):

        return create_stock_movement(
            inventory_id=validated_data['inventory'].id,
            movement_type=validated_data['type'],
            quantity=validated_data['quantity'],
            motif=validated_data.get('motif')
        )


class MouvementStockDetailSerializer(serializers.ModelSerializer):
    inventory = InventorySerializer()
    class Meta:
        model = MouvementStock
        fields = '__all__'
