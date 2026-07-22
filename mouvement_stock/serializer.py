from rest_framework import serializers
from .models import MouvementStock
from .utils import create_stock_movement


class MouvementStockSerializer(serializers.ModelSerializer):

    class Meta:
        model = MouvementStock
        fields = [
            'inventory',
            'type',
            'quantity',
            'motif'
        ]

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


class MouvementStockDetailSerializer(serializers.Serializer):
    inventory = serializers.SerializerMethodField(read_only=True)
    class Meta:
        model = MouvementStock
        fields = '__all__'
