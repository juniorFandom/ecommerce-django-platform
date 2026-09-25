from django.shortcuts import render
from rest_framework.mixins import CreateModelMixin, UpdateModelMixin, RetrieveModelMixin, DestroyModelMixin, ListModelMixin
from rest_framework.generics import GenericAPIView
from .models import Category
from .serializer import CategorySerializer, CategoryDetailSerializer

class CategoryGenericAPIView(GenericAPIView):
    lookup_field = 'slug'
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class CategoryCreateAPIView(CategoryGenericAPIView, CreateModelMixin):
    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)
    

class CategoryListAPIView(CategoryGenericAPIView, ListModelMixin):
    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

class CategorieUpdateAPIView(CategoryGenericAPIView, UpdateModelMixin):
    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)

class CategorieRetreiveAPIView(CategoryGenericAPIView, RetrieveModelMixin):
    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

class CategorieDeleteAPIView(CategoryGenericAPIView, DestroyModelMixin):
    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)
# Create your views here.

class CategorieDetailAPIView(CategoryGenericAPIView, RetrieveModelMixin):
    serializer_class = CategoryDetailSerializer
    queryset = Category.objects.prefetch_related('products')

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)