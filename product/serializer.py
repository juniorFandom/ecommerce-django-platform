from .models import Product
from rest_framework import serializers


class ProductSerializer(serializers.ModelSerializer):

    class Meta:
        model = Product

        fields = [
            'id',
            'name',
            'prix',
            'category',
            'is_active',
            'slug',
        ]

        read_only_fields = [
            'id',
            'slug',
        ]