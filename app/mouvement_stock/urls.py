from django.urls import path
from .views import (MouvementStockCreateAPIView, 
                    MouvementStockDeleteAPIView, 
                    MouvementStockDetailSerializer, 
                    MouvementStockListAPIView,
                    MouvementStockRetrieveAPIView,
                    MouvementStockUpdateAPIView)
urlpatterns = [
    path('list/', MouvementStockListAPIView.as_view(), name="list-mouvementStock"),
    path('create/', MouvementStockCreateAPIView.as_view(), name="create-mouvementStock"),
    # path('update/<slug:slug>/', MouvementStockUpdateAPIView.as_view(), name="update-mouvementStock"),
    path('delete/<slug:slug>/', MouvementStockDeleteAPIView.as_view(), name="delete-mouvementStock"),
    path('detail/<slug:slug>/', MouvementStockRetrieveAPIView.as_view(), name="detail-mouvementStock")
]