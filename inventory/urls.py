from django.urls import path
from .views import ListInventoryAPIView, InventoryCreateAPIView, UpdateInventoryAPIView, DestroyInventoryAPIView
urlpatterns = [
    path('list/',ListInventoryAPIView.as_view(), name='inventory-list'),
    path('create/',InventoryCreateAPIView.as_view(), name='inventory-create'),
    path('update/<slug:slug>',UpdateInventoryAPIView.as_view(), name='inventory-update'),
    path('delete/<slug:slug>',DestroyInventoryAPIView.as_view(), name='inventory-delete')
]