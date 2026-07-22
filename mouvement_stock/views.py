from rest_framework.mixins import (
    CreateModelMixin,
    ListModelMixin,
    UpdateModelMixin,
    RetrieveModelMixin,
    DestroyModelMixin
)
from rest_framework.generics import GenericAPIView

from .models import MouvementStock
from .serializer import (
    MouvementStockSerializer,
    MouvementStockDetailSerializer
)


class MouvementStockGenericAPIView(GenericAPIView):

    queryset = MouvementStock.objects.select_related(
        'inventory',
        'inventory__product'
    )

    lookup_field = 'slug'
    serializer_class = MouvementStockSerializer


class MouvementStockCreateAPIView(
    MouvementStockGenericAPIView,
    CreateModelMixin
):

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


class MouvementStockUpdateAPIView(
    MouvementStockGenericAPIView,
    UpdateModelMixin
):

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)


class MouvementStockListAPIView(
    MouvementStockGenericAPIView,
    ListModelMixin
):

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)


class MouvementStockDeleteAPIView(
    MouvementStockGenericAPIView,
    DestroyModelMixin
):

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)


class MouvementStockRetrieveAPIView(
    MouvementStockGenericAPIView,
    RetrieveModelMixin
):

    serializer_class = MouvementStockDetailSerializer

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)