from django.shortcuts import render
from rest_framework.generics import GenericAPIView
from rest_framework.mixins import CreateModelMixin, ListModelMixin, RetrieveModelMixin, DestroyModelMixin
from .serializer import FactureDetailSerializer, FactureSerializer


class FactureGenericApiView(GenericAPIView):
    lookup_field = 'numero'
    serializer_class = FactureSerializer

class FactureCreateApiView(FactureGenericApiView, CreateModelMixin):
    def post(self, request, *args, **kwargs):
        return self.create(self, request, *args, **kwargs)

class FactureListApiView(FactureGenericApiView, ListModelMixin):
    def get(self, request, *args, **kwargs):
        return self.list(self, request, *args, **kwargs)

class FactureRetreiveApiView(FactureGenericApiView, RetrieveModelMixin):
    serializer_class = FactureDetailSerializer
    
    def get(self, request, *args, **kwargs):
        return self.retrieve(self, request, *args, **kwargs)

class FactureDeleteApiView(FactureGenericApiView, DestroyModelMixin):
    def delete(self, request, *args, **kwargs):
        return self.destroy(self, request, *args, **kwargs)

