from asyncio import mixins

from django.shortcuts import render
from rest_framework.generics import (DestroyAPIView, GenericAPIView, 
                                    CreateAPIView,
                                    ListAPIView, 
                                    DestroyAPIView, 
                                    UpdateAPIView)
from rest_framework.mixins import (CreateModelMixin, ListModelMixin, UpdateModelMixin, DestroyModelMixin)
from .models import Product
from .serializer import ProductSerializer

class productGenericAPIView(GenericAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    lookup_field = 'slug'

class ProductCreateAPIView(CreateModelMixin,
                            productGenericAPIView):
    def post(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

class ProductListAPIView(ListModelMixin,
                        productGenericAPIView):
    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)
    
class ProductUpdateAPIView(UpdateModelMixin,
                             productGenericAPIView):
    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)

class ProductDeleteAPIView(DestroyModelMixin,
                             productGenericAPIView):
    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)


