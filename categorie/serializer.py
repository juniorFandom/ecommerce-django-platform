from rest_framework import serializers
from .models import Category
from product.serializer import ProductSerializer

class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = ['name', 'description', 'slug']
        read_only_fields = [
            'created_at',
            'updated_at',
            'slug',
            'id'
        ]


class CategoryDetailSerializer(serializers.ModelSerializer):

    products = ProductSerializer(
        many=True,
        read_only=True
    )

    class Meta:
        model = Category
        fields = [
            'id',
            'name',
            'description',
            'slug',
            'products',
        ]



