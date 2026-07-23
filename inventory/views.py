from django.shortcuts import render
from rest_framework.generics import GenericAPIView
from rest_framework.mixins import (CreateModelMixin, ListModelMixin, UpdateModelMixin, DestroyModelMixin, RetrieveModelMixin)
from inventory.serializer import InventorySerializer, InventoryCreateSerializer
from .models import Inventory

class InventoryGenericAPIView(GenericAPIView):
    queryset = Inventory.objects.select_related('product')
    serializer_class = InventorySerializer
    lookup_field = 'slug'


# class InventoryCreateAPIView(CreateModelMixin,
#                             InventoryGenericAPIView):
#     serializer_class = InventoryCreateSerializer
    
#     def post(self, request, *args, **kwargs):
#         return self.create(request, *args, **kwargs)

    

class ListInventoryAPIView(ListModelMixin,
                            InventoryGenericAPIView):
    
    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)



class RetreiveInventoryAPIView(RetrieveModelMixin, InventoryGenericAPIView):
    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)



# class UpdateInventoryAPIView(UpdateModelMixin, InventoryGenericAPIView):
#     def post(self, request, *args, **kwargs):
#         return self.update(request, *args, **kwargs)



class DestroyInventoryAPIView(DestroyModelMixin, InventoryGenericAPIView):
    def post(self, request, *args, **kwargs):
        return self.delete(request, *args, **kwargs)
