from .models import Product
from rest_framework import serializers

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = [ 'name', 'prix', 'category']
        read_only_fields = [
            'id',
            'is_active',
            'slug'
        ]