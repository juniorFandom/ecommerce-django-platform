from django.urls import path
from .views import (MouvementStockCreateAPIView, 
                    MouvementStockDeleteAPIView, 
                    MouvementStockDetailSerializer, 
                    MouvementStockListAPIView,
                    MouvementStockRetrieveAPIView,
                    MouvementStockUpdateAPIView)
urlpatterns = [
    path('MouvementStock/', MouvementStockListAPIView.as_view(), name="list-mouvementStock"),
    path('Mouvement/create/', MouvementStockCreateAPIView.as_view(), name="create-mouvementStock"),
    path('Mouvement/update/<slug:slug>/', MouvementStockUpdateAPIView.as_view(), name="update-mouvementStock"),
    path('Mouvement/delete/<slug:slug>/', MouvementStockDeleteAPIView.as_view(), name="delete-mouvementStock"),
    path('Mouvement/detail/<slug:slug>/', MouvementStockRetrieveAPIView.as_view(), name="detail-mouvementStock")
]