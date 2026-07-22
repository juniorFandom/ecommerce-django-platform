from rest_framework import serializers
from .models import Inventory
from product.serializer import ProductSerializer
from product.models import Product


class InventorySerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)
    is_available = serializers.SerializerMethodField()
    product_id = serializers.PrimaryKeyRelatedField(
        queryset=Product.objects.all(),
        source='product',
        write_only=True
    )

    class Meta:
        model = Inventory
        fields = [
            'id',
            'product',
            'product_id',
            'quantity',
            'reserved_quantity',
            'minimum_stock',
            'last_updated',
            'slug',
            'is_available'
        ]

    
    def get_is_available(self,obj):
        return obj.available_quantity
    

class InventoryCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Inventory
        fields = ['product','quantity','minimum_stock']


    def validate(self, attrs):
        quantity = attrs.get('quantity')
        minimum_stock = attrs.get('minimum_stock')

        if quantity <= minimum_stock:
            raise serializers.ValidationError({
                'quantity': 'La quantité doit être supérieure à la quantité minimum.'
            })

        return attrs