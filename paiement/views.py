from django.shortcuts import render
from rest_framework.generics import GenericAPIView
from .serializer import PaiementSerializer
from rest_framework.mixins import  CreateModelMixin, ListModelMixin, RetrieveModelMixin, DestroyModelMixin

# Create your views here.
class PaiementView(GenericAPIView, CreateModelMixin, ListModelMixin, RetrieveModelMixin, DestroyModelMixin):

    """
    Vue pour la gestion des paiements.
    """

    serializer_class = PaiementSerializer
    lookup_field = "reference"

    def post(self, request, *args, **kwargs):
        
        ''''
        Crée un nouveau paiement pour une commande donnée.
        '''
        return self.create(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        
        '''
        Récupère la liste de tous les paiements ou un paiement spécifique par référence.
        '''
        if 'reference' in kwargs:
            return self.retrieve(request, *args, **kwargs)
        return self.list(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        
        '''
        Supprime un paiement spécifique par référence.
        '''
        return self.destroy(request, *args, **kwargs)


