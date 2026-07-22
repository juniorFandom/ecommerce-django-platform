from django.urls import path
from .views import ListInventoryAPIView, InventoryCreateAPIView, UpdateInventoryAPIView, DestroyInventoryAPIView
urlpatterns = [
    path('Inventory/',ListInventoryAPIView.as_view(), name='inventory-list'),
    path('create/Inventory',InventoryCreateAPIView.as_view(), name='inventory-create'),
    path('update/Inventory',UpdateInventoryAPIView.as_view(), name='inventory-update'),
    path('delete/Inventory',DestroyInventoryAPIView.as_view(), name='inventory-delete')
]