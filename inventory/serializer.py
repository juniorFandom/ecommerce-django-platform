from rest_framework import serializers
from .models import Inventory
from product.serializer import ProductSerializer
from product.models import Product
from .service import create_inventory


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
        return obj.is_available
    

class InventoryCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Inventory
        fields = ['product','quantity','minimum_stock','slug']
        read_only_fields = [
            'id',
            'reserved_quantity',
            'last_updated',
            'slug'
        ]

    def create(self, validated_data):
        print(f'dans la methode de validation de l\inventory {validated_data}')
        return create_inventory(**validated_data)
