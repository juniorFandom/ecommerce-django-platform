from .models import Product
from rest_framework import serializers


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product

        fields = ['category','name', 'prix','slug','id']

        read_only_fields = [
            'slug',
            'is_active',
            'id'
        ]
