from django.db.models import Prefetch
from rest_framework.generics import GenericAPIView
from rest_framework.mixins import (
    CreateModelMixin,
    ListModelMixin,
    RetrieveModelMixin,
    UpdateModelMixin,
    DestroyModelMixin
)

from .models import Commande, LigneCommande
from .serializer import CommandeSerializer


class CommandeGenericAPIView(GenericAPIView):
    serializer_class = CommandeSerializer
    lookup_field = "slug"

    queryset = Commande.objects.prefetch_related("lignes")


class CreateCommandeAPIView(
    CommandeGenericAPIView,
    CreateModelMixin
):

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


class ListCommandeAPIView(
    CommandeGenericAPIView,
    ListModelMixin
):

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)


class RetrieveCommandeAPIView(
    CommandeGenericAPIView,
    RetrieveModelMixin
):

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)


class UpdateCommandeAPIView(
    CommandeGenericAPIView,
    UpdateModelMixin
):

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)


class DeleteCommandeAPIView(
    CommandeGenericAPIView,
    DestroyModelMixin
):

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)
